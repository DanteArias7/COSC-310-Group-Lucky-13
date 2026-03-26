"""User service layer for user business logic"""
from typing import Any, Dict, List, Protocol
import uuid

from fastapi import HTTPException
from app.schemas.user import User, UserCreate, UserUpdate

class UserServices():
    """User Service Class containg methods related to the business logic around
    viewing, creating, deleting, and updating user profiles"""

    def __init__(self, repo: IUserRepo):
        """Initialize instance with repo object"""
        self.repo = repo

    def get_user_by_id(self, user_id: str) -> User:
        """
        Gets a users information whose ID matches the given ID

        Args:
            user_id: The ID of the user's info being requested

        Returns:
            A User object matching the given ID
        """
        users = self.repo.load_all_users()

        for user in users:
            if user["id"] == user_id:
                return User(**user)

        raise HTTPException(status_code=404,
                            detail=f"User {user_id} not found")

    def create_user(self, new_user: UserCreate) -> User:
        """
        Creates a new user and stores it in the data store

        Args:
            new_user: A UserCreate object containing the information
            of the user being created.

        Returns:
            The new User object
        """
        new_id = str(uuid.uuid4())
        new_user = User(id=new_id,
                    name=new_user.name.strip(),
                    email=new_user.email.strip(),
                    phone_number=new_user.phone_number.strip(),
                    address=new_user.address.strip(),
                    password=new_user.password.strip(),
                    role=new_user.role.strip()
                    )

        user = new_user.model_dump()
        self.repo.save_user(user)
        return new_user

    def update_user(self, user_id: str, updated_user: UserUpdate) -> User:
        """
        Updates user information in the data store

        Args:
            user_id: The ID of the user's info being updated
            updated_user: A UserUpdate object containing the
            updated information

        Returns:
            A the updated User object

        Raises:
            A 404 HTTPException if the user is not found
        """
        users = self.repo.load_all_users()

        for i, user in enumerate(users):
            if user["id"] == user_id:
                users[i] = {"id" : user_id} | updated_user.model_dump()
                self.repo.save_all_users(users)
                return User(**users[i])

        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")

    def delete_user(self, user_id: str) -> None:
        """
        Deletes user from the data store

        Args:
            user_id: The ID of the user's info being deleted

        Returns:
            A the updated User object

        Raises:
            A 404 HTTPException if the user is not found
        """

        users = self.repo.load_all_users()

        for user in users:
            if user["id"] == user_id:
                users.remove(user)
                self.repo.save_all_users(users)
                return

        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")

class IUserRepo(Protocol):
    """User Service Class"""
    def load_all_users(self) -> List[Dict[str, Any]]:
        """Load all users from the data store"""
    def save_user(self, user : Dict[str : any]) -> None:
        """Save a user to the datastore"""
    def save_all_users(self, user : List[Dict[str : any]]) -> None:
        """Save all users to the data store"""
