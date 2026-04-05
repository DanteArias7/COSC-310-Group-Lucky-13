"""API Endpoints for favorite functionality"""
from pathlib import Path
from fastapi import APIRouter

FAVORITE_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "favorites.json"

favorite_router = APIRouter(
    prefix="/favorites",
    tags=["favorites"]
)
