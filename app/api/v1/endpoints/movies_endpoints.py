from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.core.database import get_db
from app.repositories.movie_repository import MovieRepository
from app.services.movie_service import MovieService
from app.schemas.movie_schema import MovieCreate, MovieUpdate, MovieResponse

router = APIRouter()

def get_movie_service(db: Session = Depends(get_db)):
    """Dependency to get movie service with database session"""
    repository = MovieRepository(db)
    return MovieService(repository)


# ============ CRUD ENDPOINTS ============

@router.post("/addmovies", response_model=MovieResponse, status_code=201)
async def add_movie(
    movie: MovieCreate,
    service: MovieService = Depends(get_movie_service)
):
    """Add a new movie to your watchlist"""
    try:
        return service.add_movie(movie)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/movies", response_model=List[MovieResponse])
async def get_movies(
    genre: Optional[str] = None,
    year: Optional[int] = None,
    sort_by: Optional[str] = Query(None, regex="^(title|rating|year)$"),
    sort_desc: bool = False,
    service: MovieService = Depends(get_movie_service)
):
    """Get all movies with optional filtering and sorting"""
    try:
        movies = service.filter_movies(genre, year)
        
        if sort_by:
            movies.sort(key=lambda m: getattr(m, sort_by), reverse=sort_desc)
        
        return movies
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/movies/{movie_id}", response_model=MovieResponse)
async def get_movie(
    movie_id: int,
    service: MovieService = Depends(get_movie_service)
):
    """Get a single movie by ID"""
    try:
        return service.get_movie_by_id(movie_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/movies/{movie_id}", response_model=MovieResponse)
async def update_movie(
    movie_id: int,
    movie_update: MovieUpdate,
    service: MovieService = Depends(get_movie_service)
):
    """Update a movie by ID"""
    try:
        return service.update_movie(movie_id, movie_update)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/movies/{movie_id}", status_code=204)
async def delete_movie(
    movie_id: int,
    service: MovieService = Depends(get_movie_service)
):
    """Delete a movie by ID"""
    try:
        service.delete_movie(movie_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ============ SEARCH & FILTER ENDPOINTS ============

@router.get("/movies/search", response_model=List[MovieResponse])
async def search_movies(
    q: str = Query(..., min_length=2, description="Search query (min 2 characters)"),
    service: MovieService = Depends(get_movie_service)
):
    """Search movies by title (case-insensitive)"""
    try:
        return service.search_movies(q)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/movies/filter/genre/{genre}", response_model=List[MovieResponse])
async def filter_by_genre(
    genre: str,
    service: MovieService = Depends(get_movie_service)
):
    """Get movies by genre"""
    try:
        return service.filter_movies(genre=genre)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/movies/filter/year/{year}", response_model=List[MovieResponse])
async def filter_by_year(
    year: int,
    service: MovieService = Depends(get_movie_service)
):
    """Get movies by year"""
    try:
        return service.filter_movies(year=year)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/movies/top-rated/", response_model=List[MovieResponse])
async def get_top_rated(
    limit: int = Query(5, ge=1, le=50, description="Number of movies to return"),
    service: MovieService = Depends(get_movie_service)
):
    """Get top rated movies"""
    return service.get_top_rated(limit)


@router.get("/movies/director/{director}", response_model=List[MovieResponse])
async def get_by_director(
    director: str,
    service: MovieService = Depends(get_movie_service)
):
    """Get movies by director name (partial match)"""
    try:
        return service.get_by_director(director)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))