from pydantic import BaseModel
from  typing import Optional
from datetime import datetime

class MovieBase(BaseModel):
    title: str
    year: int
    genre: str 
    rating: float 
    director : str
    watched: bool=False

class MovieCreate(MovieBase):
    pass 

class MovieUpdate(BaseModel):
    title:Optional[str]=None
    year:Optional[ int]=None
    genre: Optional[str]=None
    rating: Optional[float] =None
    director : Optional[str]=None
    watched: Optional[bool]=None


class MovieResponse(MovieBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]=None

    class Config:
        from_attributes=True