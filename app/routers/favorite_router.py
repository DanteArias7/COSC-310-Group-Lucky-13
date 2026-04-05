"""API Endpoints for favorite functionality"""

from fastapi import APIRouter

favorite_router = APIRouter(
    prefix="/favorites",
    tags=["favorites"]
)
