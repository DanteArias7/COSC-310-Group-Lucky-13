"""User Repository Layer"""
from pathlib import Path
import json
from typing import Dict, Any

#pylint: disable=too-few-public-methods
class UserRepo():
    """User Repository methods"""
    def __init__(self, data_path: Path):
        self.data_path = data_path

    def save_user(self, user: Dict[str, Any]) -> None:
        """Save user to json file"""
        if not Path(self.data_path).is_file():
            with open(self.data_path, "w", encoding="utf-8") as f:
                empty_list = []
                json.dump(empty_list, f, indent=2)

        with open(self.data_path, "r",encoding="utf-8") as f:
            users = json.load(f)

        users.append(user)

        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2)
