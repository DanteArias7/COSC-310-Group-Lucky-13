"""User API endpoints"""
from pathlib import Path

from fastapi import APIRouter, Depends
from app.schemas.user import User, UserCreate
from app.services.user_services import UserServices
from app.repositories.user_repo import UserRepo

user_router = APIRouter(prefix="/users", tags=["user"])
USER_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "users.json"

def create_user_repo():
    """"Initialize repo object with data path to user json file"""
    return UserRepo(USER_DATA_PATH)

@user_router.post("", response_model=User, status_code=201)
def add_user(payload: UserCreate, repo: UserRepo = Depends(create_user_repo)):
    """API endpoint to create a user"""
    user_service = UserServices(repo)
    return user_service.create_user(payload)
