"""User API endpoints"""
from fastapi import APIRouter
from app.schemas.user import User, UserCreate
from app.services.user_services import UserServices
from app.repositories.user_repo import UserRepo

user_router = APIRouter(prefix="/users", tags=["user"])

@user_router.post("", response_model=User, status_code=201)
def add_user(payload: UserCreate):
    """API endpoint to create a user"""
    repo = UserRepo()
    user_service = UserServices(repo)
    return user_service.create_user(payload)
