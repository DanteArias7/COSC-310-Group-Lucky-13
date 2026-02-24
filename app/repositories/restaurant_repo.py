"""Repository layer for restaurant data."""

import json
from pathlib import Path
from typing import Any, Dict, List

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
