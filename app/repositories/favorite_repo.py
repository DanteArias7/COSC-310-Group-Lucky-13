"""Repository for managing user favorites."""

import json
import os
from pathlib import Path
from typing import Any, Dict, List

# pylint: disable=duplicate-code
class FavoriteRepo():
    """Favorite repository methods"""
    def __init__(self, data_path: Path):
        self.data_path = data_path

    def load_all_favorites(self) -> List[Dict[str, Any]]:
        """Return all favorites in a list"""
        if not self.data_path.exists():
            return []

        with open(self.data_path, "r", encoding ="utf-8") as f:
            return json.load(f)

    def save_all_favorites(self, favorites: List[Dict[str,Any]]) -> None:
        """Save all favorites to json file"""
        temp_favorite_file = self.data_path.with_suffix(".tmp")
        with open(temp_favorite_file, "w", encoding="utf-8") as f:
            json.dump(favorites, f, ensure_ascii=False, indent=2)
        os.replace(temp_favorite_file, self.data_path)
