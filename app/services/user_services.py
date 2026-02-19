"""User service layer for user business logic"""
from typing import Protocol
import uuid
from sqlmodel import SQLModel
from app.schemas.user import User, UserCreate

# pylint: disable=too-few-public-methods
class UserServices():
    """User Service Class"""
    def __init__(self, repo: IUserRepo):
        """Initialize instance with repo object"""
        self.repo = repo

    def create_user(self, payload: UserCreate):
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
        self.repo.save_user(new_user)
        return new_user

class IUserRepo(Protocol):
    """User Service Class"""
    def save_user(self, user : SQLModel) -> None:
        """save a user"""  
