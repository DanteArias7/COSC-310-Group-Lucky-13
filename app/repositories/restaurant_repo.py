"""Repository layer for restaurant data."""

import json
from pathlib import Path

FILE_PATH = Path("app/data/restaurants.json")


def get_all_restaurants():
    """Return all restaurants"""
    if not FILE_PATH.exists():
        return []

    with open(FILE_PATH, "r", encoding ="utf-8") as f:
        return json.load(f)


def get_restaurant_by_id(restaurant_id: str):
    """ Return restaurant by id """
    restaurants = get_all_restaurants()
    for restaurant in restaurants:
        if str(restaurant["id"]) == str(restaurant_id):
            return restaurant
    return None
