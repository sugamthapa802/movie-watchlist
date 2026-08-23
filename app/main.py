from fastapi import FastAPI
from app.core.database import engine, Base
from app.models.movie import Movie
from app.api.v1.endpoints.movies_endpoints import router  # ← IMPORT THE ROUTER!

# Create database tables
print("🔄 Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully!")

app = FastAPI(
    title="Movie Watchlist API",
    description="API for managing your movie watchlist",
    version="1.0.0"
)

# ✅ THIS LINE IS CRUCIAL - Register the router!
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Welcome to Movie Watchlist API",
        "docs": "/docs",
        "redoc": "/redoc",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}