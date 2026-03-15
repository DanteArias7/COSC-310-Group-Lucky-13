"""User API endpoints"""
from pathlib import Path

from fastapi import APIRouter, Depends, Header
from fastapi import status
from app.schemas.user import User, UserCreate, UserUpdate
from app.services.authorization_services import AuthorizationServices
from app.services.user_services import UserServices
from app.repositories.user_repo import UserRepo

user_router = APIRouter(prefix="/users", tags=["user"])
USER_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "users.json"

def create_user_repo():
    """"Initialize repo object with data path to user json file"""
    return UserRepo(USER_DATA_PATH)

@user_router.get("/{user_id}", response_model=User, status_code=200)
def get_user_by_id(user_id: str, user_repo: UserRepo = Depends(create_user_repo),
             current_user_id = Header(...,alias="user-id"),):
    """API endpoint to get a user by their id

    Args:
        user_repo: UserRepo object to allow user_service to access user data store
        user_id: The ID of the user making the request

    Returns:
        A user object who's id matches the given ID

    Raises: 404 HTTPexception if user is not found"""
    user_service = UserServices(user_repo)
    authorization_service = AuthorizationServices(user_repo)
    authorization_service.authorize(user_id, "manage_own_account")
    authorization_service.authorize_access(current_user_id, user_id)
    return user_service.get_user_by_id(user_id)

@user_router.post("", response_model=User, status_code=201)
def add_user(payload: UserCreate, repo: UserRepo = Depends(create_user_repo)):
    """API endpoint to create a user"""
    user_service = UserServices(repo)
    return user_service.create_user(payload)

@user_router.put("/{user_id}", response_model=User, status_code=200)
def update_user(user_id, payload: UserUpdate, repo: UserRepo = Depends(create_user_repo),
                current_user_id: str = Header(...,alias="user-id")):
    """API endpoint to update a user"""
    user_service = UserServices(repo)
    authorization_service = AuthorizationServices(repo)
    authorization_service.authorize(current_user_id, "manage_own_account")
    authorization_service.authorize_access(current_user_id, user_id)
    return user_service.update_user(user_id, payload)

@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id, repo: UserRepo = Depends(create_user_repo),
                current_user_id: str = Header(...,alias="user-id")):
    """API endpoint to delete a user"""
    user_service = UserServices(repo)
    authorization_service = AuthorizationServices(repo)
    authorization_service.authorize(current_user_id, "manage_own_account")
    authorization_service.authorize_access(current_user_id, user_id)
    return user_service.delete_user(user_id)
