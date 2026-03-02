
"""Repository layer for restaurant data."""

import json
import os
from pathlib import Path
from typing import Any, Dict, List

#pylint: disable=too-few-public-methods
class RestaurantRepo():
    """Restaurant repository methods"""
    def __init__(self, data_path: Path):
        self.data_path = data_path

    def load_all_restaurants(self) -> List[Dict[str, Any]]:
        """Return all restaurants"""
        if not self.data_path.exists():
            return []

        with open(self.data_path, "r", encoding ="utf-8") as f:
            return json.load(f)

    def save_all_restaurants(self, restaurants: List[Dict[str,Any]]) -> None:
        """Save all restaurants to json file"""
        temp_restaurant_file = self.data_path.with_suffix(".tmp")
        with open(temp_restaurant_file, "w", encoding="utf-8") as f:
            json.dump(restaurants, f, ensure_ascii=False, indent=2)
        os.replace(temp_restaurant_file, self.data_path)
