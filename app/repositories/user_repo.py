"""User Repository Layer"""
import os
from pathlib import Path
import json
from typing import Dict, Any, List

#pylint: disable=too-few-public-methods
class UserRepo():
    """User Repository methods"""
    def __init__(self, data_path: Path):
        self.data_path = data_path
    
    def load_all_users(self) -> List[Dict[str, Any]]:
        """Load all users from the json file"""
        if not Path(self.data_path).is_file():
            with open(self.data_path, "w", encoding="utf-8") as f:
                empty_list = []
                json.dump(empty_list, f, ensure_ascii=False, indent=2)

        with open(self.data_path, "r") as f:
            users = json.load(f)
        return users
    
    
    def save_user(self, user: Dict[str, Any]) -> None:
        """Save user to json file"""
        users = self.load_all_users()

        users.append(user)

        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

    def save_all_users(self, users: List[Dict[str,Any]]) -> None:
        temp_user_file = self.data_path.with_suffix(".tmp")
        with open(temp_user_file, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
        os.replace(temp_user_file, self.data_path)