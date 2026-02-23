"""User service layer for user business logic"""
from typing import Any, Dict, List, Protocol
import uuid

from fastapi import HTTPException
from app.schemas.user import User, UserCreate, UserUpdate

# pylint: disable=too-few-public-methods
class UserServices():
    """User Service Class"""
    def __init__(self, repo: IUserRepo):
        """Initialize instance with repo object"""
        self.repo = repo

    def create_user(self, payload: UserCreate) -> User:
        """Create a new user"""
        new_id = str(uuid.uuid7())
        new_user = User(id=new_id,
                    name=payload.name.strip(),
                    email=payload.email.strip(),
                    phone_number=payload.phone_number.strip(),
                    address=payload.address.strip(),
                    password=payload.password.strip(),
                    role=payload.role.strip()
                    )

        user = new_user.model_dump()
        self.repo.save_user(user)
        return new_user

    def update_user(self, user_id: str, payload: UserUpdate) -> User:
        users = self.repo.load_all_users()

        for i, user in enumerate(users):
            if user["id"] == user_id:
                users[i] = {"id" : user_id} | payload.model_dump()
                self.repo.save_all_users(users)
                return User(**users[i])
            
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")

class IUserRepo(Protocol):
    """User Service Class"""
    def load_all_users(self) -> List[Dict[str, Any]]:
        """save a user"""  
    def save_user(self, user : Dict[str : any]) -> None:
        """save a user""" 
    def save_all_users(self, user : List[Dict[str : any]]) -> None:
        """save a user""" 
