from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import String, Float, DateTime,Integer,Boolean
from typing import List
from app.core.database import Base
from sqlalchemy.sql import func

class Movie(Base):
    __tablename__="movies"
    id:Mapped[Integer]= mapped_column(Integer,primary_key=True)
    title:Mapped[String]= mapped_column(String(100))
    year: Mapped[Integer]= mapped_column(Integer,nullable=False)
    genre: Mapped[String]= mapped_column(String(100),nullable=False)
    director:Mapped[String]=mapped_column(String(100), nullable=False)
    rating:Mapped[Float]=mapped_column(Float) 
    watched:Mapped[Boolean]=mapped_column(Boolean,default=False)

    #TimeStamps
    created_at:Mapped[DateTime]=mapped_column(DateTime,server_default=func.now())
    updated_at:Mapped[DateTime]=mapped_column(DateTime,onupdate=func.now())
    def __repr__(self):
        return f"<Movie(id={self.id}, title='{self.title}')>"
    