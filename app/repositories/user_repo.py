"""User Repository Layer"""
from pathlib import Path
import json
from typing import Dict, Any

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "users.json"

#pylint: disable=too-few-public-methods
class UserRepo():
    """User Repository methods"""
    def save_user(self, user: Dict[str, Any]) -> None:
        """Save user to json file"""
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(user, f, indent=2)
