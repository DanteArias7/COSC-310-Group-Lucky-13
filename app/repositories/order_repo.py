"""Repository layer for order data."""
from pathlib import Path
from typing import Any, Dict, List
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
        orders = pandas.read_csv(self.data_path)

        return orders.to_dict(orient="records")

    def save_order(self, order: Dict[str, Any]) -> None:
        """Saves an order object to the order csv file

        Args:
            order: An Order object in dict form

        Returns: Nothing"""
        orderdf = pandas.DataFrame([order])
        orderdf.to_csv(self.data_path, mode="a", index=False, header=False)
