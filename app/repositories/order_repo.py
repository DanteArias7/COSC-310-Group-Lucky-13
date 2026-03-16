# pylint: disable=trailing-whitespace
"""Repository layer for order data."""
from pathlib import Path
from typing import Any, Dict, List, Optional
import json
import os
import pandas

#pylint: disable=too-few-public-methods
class OrderRepo():
    """Order repository methods"""
    def __init__(self, data_path: Path):
        """Initializes OrderRepo Object with data path to order csv file

        Args:
            data_path: data path to orders csv file"""
        self.data_path = data_path

    def load_all_orders(self) -> List[Dict[str, Any]]:
        """Loads all orders from csv file

        Returns: All orders in as  List of Dicts."""
        orders = pandas.read_csv(self.data_path, keep_default_na=False)

        return orders.to_dict(orient="records")

    def save_order(self, order: Dict[str, Any]) -> None:
        """Saves an order object to the order csv file

        Args:
            order: An Order object in dict form

        Returns: Nothing"""
        orderdf = pandas.DataFrame([order])
        orderdf.to_csv(self.data_path, mode="a", index=False, header=False)

    def update_orders(self, orders: List[Dict[str, Any]]) -> None:
        """Overwrites the order csv file

        Args:
            orders: A list of Order objects in dict form

        Returns: Nothing"""
        orderdf = pandas.DataFrame(orders)
        orderdf.to_csv(self.data_path, index=False)

    def get_order_by_id(self, order_id: str) -> Optional[Dict[str, Any]]:
        """Return a single order dict by ID, or None if not found."""
        orders = self.load_all_orders()
        for order in orders:
            if order["id"] == order_id:
                return order
        return None
    
    def save_all_orders(self, orders: List[Dict[str, Any]]) -> None:
        """Overwrite all orders atomically using a temp file."""
        self._write(orders)

    def _write(self, orders: List[Dict[str, Any]]) -> None:
        """Write orders list to disk atomically."""
        temp_path = self.data_path.with_suffix(".tmp")
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(orders, f, ensure_ascii=False, indent=2)
        os.replace(temp_path, self.data_path)
