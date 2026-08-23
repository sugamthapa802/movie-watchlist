from app.repositories.movie_repository import MovieRepository
from app.schemas.movie_schema import MovieCreate, MovieResponse, MovieUpdate
from typing import List, Dict, Optional
from datetime import datetime

class MovieService:
    def __init__(self, repository:MovieRepository):
        self.repository=repository


    def add_movie(self,movie_data: MovieCreate) -> MovieResponse:
        if not self.validate_movie_data(movie_data):
            return
        return self.repository.add(movie_data)

    def validate_movie_data(self,movie_data: MovieCreate)-> bool:
        if not (movie_data.year) or not (movie_data.title) or not (movie_data.genre) or not (movie_data.rating) or not (movie_data.director):
            raise ValueError("Missing value")
        current_year = datetime.now().year
        if not movie_data.year:
            raise ValueError("Year is required")
        if movie_data.year < 1888:  # First movie ever made
            raise ValueError("Year must be 1888 or later")
        if movie_data.year > current_year:
            raise ValueError(f"Year cannot be in the future (max: {current_year})")
        
        # Genre validation
        if not movie_data.genre or not movie_data.genre.strip():
            raise ValueError("Genre is required")
        
        # Rating validation
        if movie_data.rating is None:
            raise ValueError("Rating is required")
        if not 1 <= movie_data.rating <= 10:
            raise ValueError("Rating must be between 1 and 10")
        
        # Director validation
        if not movie_data.director or not movie_data.director.strip():
            raise ValueError("Director is required")
        
        return True

       
    def get_all_movies(self) -> List[MovieResponse]:
        """Get all movies"""
        return self.repository.get_all()
    
    def get_movie_by_id(self, movie_id: int) -> MovieResponse:
        """Get a single movie by ID"""
        movie = self.repository.get_by_id(movie_id)
        if not movie:
            raise ValueError(f"Movie with ID {movie_id} not found")
        return movie
    
    def update_movie(self, movie_id: int, update_data: MovieUpdate) -> MovieResponse:
        """Update a movie with business rules"""
        
        # Check if movie exists first
        existing = self.repository.get_by_id(movie_id)
        if not existing:
            raise ValueError(f"Movie with ID {movie_id} not found")
        
        # Business Rule: If rating is being updated, validate it
        if update_data.rating is not None:
            if not (1 <= update_data.rating <= 10):
                raise ValueError("Rating must be between 1 and 10")
        
        # Business Rule: If year is being updated, validate it
        if update_data.year is not None:
            current_year = datetime.now().year
            if update_data.year > current_year:
                raise ValueError(f"Year cannot be in the future (max: {current_year})")
            if update_data.year < 1888:
                raise ValueError("Year must be 1888 or later")

        
        # All rules passed → update
        updated = self.repository.update(movie_id, update_data)
        if not updated:
            raise ValueError(f"Movie with ID {movie_id} not found")
        return updated
    
    def delete_movie(self, movie_id: int) -> bool:
        """Delete a movie"""
        # Check if movie exists first
        existing = self.repository.get_by_id(movie_id)
        if not existing:
            raise ValueError(f"Movie with ID {movie_id} not found")
        
        return self.repository.delete(movie_id)
    
    def search_movies(self, query: str) -> List[MovieResponse]:
        """Search movies by title"""
        if not query or len(query.strip()) < 2:
            raise ValueError("Search query must be at least 2 characters")
        return self.repository.search_by_title(query.strip())
    
    def filter_movies(self, genre: Optional[str] = None, year: Optional[int] = None) -> List[MovieResponse]:
        """Filter movies by genre and/or year"""
        
        # Validate genre if provided
        if genre:
            allowed_genres = ["Action", "Drama", "Comedy", "Sci-Fi", "Horror", 
                             "Romance", "Thriller", "Documentary", "Animation", 
                             "Fantasy", "Mystery", "Crime"]
            if genre not in allowed_genres:
                raise ValueError(f"Genre must be one of: {', '.join(allowed_genres)}")
        
        # Validate year if provided
        if year:
            current_year = datetime.now().year
            if year > current_year:
                raise ValueError(f"Year cannot be in the future (max: {current_year})")
            if year < 1888:
                raise ValueError("Year must be 1888 or later")
        
        # Get all movies and filter
        movies = self.repository.get_all()
        
        if genre:
            movies = [m for m in movies if m.genre.lower() == genre.lower()]
        if year:
            movies = [m for m in movies if m.year == year]
        
        return movies
    
    def toggle_watched(self, movie_id: int) -> MovieResponse:
        """Toggle the watched status of a movie"""
        movie = self.repository.get_by_id(movie_id)
        if not movie:
            raise ValueError(f"Movie with ID {movie_id} not found")
        
        update_data = MovieUpdate(watched=not movie.watched)
        return self.update_movie(movie_id, update_data)
    
    def get_top_rated(self, limit: int = 5) -> List[MovieResponse]:
        """Get top rated movies"""
        movies = self.repository.get_all()
        movies.sort(key=lambda m: m.rating, reverse=True)
        return movies[:limit]
    
    def get_by_director(self, director: str) -> List[MovieResponse]:
        """Get movies by director"""
        if not director or len(director.strip()) < 2:
            raise ValueError("Director name must be at least 2 characters")
        
        movies = self.repository.get_all()
        return [m for m in movies if director.lower() in m.director.lower()]