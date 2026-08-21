from fastapi import FastAPI
from app.core.database import Base, engine
from app.models.movie import Movie



app=FastAPI()

Base.metadata.create_all(bind=engine)