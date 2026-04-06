"""API Endpoints for favorite functionality"""
from pathlib import Path
from fastapi import APIRouter

from app.repositories.favorite_repo import FavoriteRepo

FAVORITE_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "favorites.json"

favorite_router = APIRouter(
    prefix="/favorites",
    tags=["favorites"]
)

def create_favorite_repo():
    """ Initializes the FavoriteRepo with the path to the favorites data file.
    Returns:
        FavoriteRepo: An instance of the FavoriteRepo class.
    """
    return FavoriteRepo(FAVORITE_DATA_PATH)
