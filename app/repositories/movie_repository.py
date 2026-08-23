from app.models.movie import Movie
from sqlalchemy.orm import Session
from app.schemas.movie_schema import MovieCreate, MovieResponse, MovieUpdate
from typing import Optional, List

class MovieRepository:
    def __init__(self,db:Session):
        self.db=db

    def add(self,movie_data:MovieCreate) -> MovieResponse :
        db_movie= Movie(**movie_data.model_dump())
        self.db.add(db_movie)
        self.db.commit()
        self.db.refresh(db_movie)

        return MovieResponse.model_validate(db_movie)

    def get_by_id(self,movie_id: int) -> Optional[MovieResponse]:
        db_movie=self.db.query(Movie).filter(Movie.id==movie_id).first()
        if db_movie:
            return MovieResponse.model_validate(db_movie)
        else:
            None


    def get_all(self) -> List[MovieResponse]:
        db_movies= self.db.query(Movie).all()
        return [MovieResponse.model_validate(movie)for movie in db_movies]

    def update(self,movie_id: int,update_data: MovieUpdate) -> MovieResponse :
        db_movie=self.db.query(Movie).filter(Movie.id==movie_id).first()
        if not db_movie:
            return None
        update_dict=update_data.model_dump(exclude_unset=True)
        for key,value in update_dict.items():
            setattr(db_movie,key,value)
        self.db.commit()
        self.db.refresh(db_movie)
        return MovieResponse.model_validate(db_movie)

    def delete(self,movie_id:int)-> bool:
        db_movie=self.db.query(Movie).filter(Movie.id==movie_id).first()
        if not db_movie:
            return False
        self.db.delete(db_movie)
        self.db.commit()
        return True

    def search_by_title(self,movie_name:str) -> MovieResponse:
        db_movie=self.db.query(Movie).filter(Movie.title.ilike(f"%{movie_name}")).first()
        return MovieResponse.model_validate(db_movie)

    
    def filter_by_genre(self, genre: str) -> List[MovieResponse]:
        """Filter movies by genre"""
        db_movies = self.db.query(Movie).filter(
            Movie.genre.ilike(genre)
        ).all()
        return [MovieResponse.model_validate(m) for m in db_movies]
    
    def filter_by_year(self, year: int) -> List[MovieResponse]:
        """Filter movies by year"""
        db_movies = self.db.query(Movie).filter(Movie.year == year).all()
        return [MovieResponse.model_validate(m) for m in db_movies]