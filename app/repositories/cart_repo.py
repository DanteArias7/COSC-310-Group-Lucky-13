"""Repository layer for cart data."""

import json
import os
from pathlib import Path
from typing import Any, Dict, List

#pylint: disable=duplicate-code
class CartRepo():
    """Cart repository methods"""
    def __init__(self, data_path: Path):
        self.data_path = data_path

    def load_all_carts(self) -> List[Dict[str, Any]]:
        """Return all carts in a list"""
        if not self.data_path.exists():
            return []

        with open(self.data_path, "r", encoding ="utf-8") as f:
            return json.load(f)

    def save_all_carts(self, carts: List[Dict[str,Any]]) -> None:
        """Save all carts to json file"""
        temp_cart_file = self.data_path.with_suffix(".tmp")
        with open(temp_cart_file, "w", encoding="utf-8") as f:
            json.dump(carts, f, ensure_ascii=False, indent=2)
        os.replace(temp_cart_file, self.data_path)
