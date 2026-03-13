"""Service layer for restaurant business logic."""

from datetime import date
from typing import Any, Dict, List, Protocol
import random
import uuid
from fastapi import HTTPException
from app.schemas.menu import MenuItem, UpdateMenuItem
from app.schemas.restaurant import RestaurantResult, Restaurant, RestaurantCreate, UpdateRestaurant

class RestaurantServices():
    """Restaurant service methods"""
    def __init__(self, repo: IRestaurantRepo):
        """Initialize instance with repo object"""
        self.repo = repo

    def create_new_restaurant(self, user_id: str, payload: RestaurantCreate) -> Restaurant:
        """
        Create new restaurant profile
        Rules:
        - menu is always initialized as an empty list (restaurant should be created before
            MenuItems are added)

        Args:
            name: name of the restaurant
            hours: dictionary of [day: hours] the restaurant is open for every day of the week
            phone_number: phone number for the restaurant
            address: where the restaurant is located
            tags: types of cuisine(s), dietary restrictions (vegan, gluten free, etc)
                accommodated, type of food (brunch, cafe, etc)
            menu: list of MenuItems offered by the restaurant, initalized as empty list

        Returns:
            new Restaurant object
        """
        restaurant = Restaurant(
            id=random.randint(1, 1_000_000),
            user_id=user_id,
            name=payload.name,
            hours=payload.hours,
            phone_number=payload.phone_number,
            address=payload.address,
            tags=payload.tags,
            menu= payload.menu,
        )
        restaurants = self.repo.load_all_restaurants()
        restaurants.append(restaurant.model_dump())
        self.repo.save_all_restaurants(restaurants)
        return restaurant

    def fetch_all_restaurants(self) -> List[RestaurantResult]:
        """
        Gets a representation of all restaurant objects

        Returns:
            A list of restaurantResult objects
        """

        full_restaurants = self.repo.load_all_restaurants()
        restaurants = []
        today = date.today().strftime("%A")

        for restaurant in full_restaurants:
            restaurant = RestaurantResult(
                        id=restaurant["id"],
                        name=restaurant["name"],
                        address=restaurant["address"],
                        todays_hours=restaurant["hours"][today],
                        tags=restaurant["tags"]
                        )
            restaurants.append(restaurant)

        return restaurants

    def fetch_name_searched_restaurants(self, search: str) -> List[RestaurantResult]:
        """Gets restaurants based on a given search term string

        Args:
        search: A string used to compare to the restaurants name

        Returns:
        A list of RestaurantResult Objects where the restaurant's name contains the search string.
        """
        restaurants = self.repo.load_all_restaurants()
        results = []
        today = date.today().strftime("%A")

        for restaurant in restaurants:
            if search.lower() in restaurant["name"].lower():
                result = RestaurantResult(id=restaurant["id"],
                                  name=restaurant["name"],
                                  address=restaurant["address"],
                                  todays_hours=restaurant["hours"][today],
                                  tags=restaurant["tags"])
                results.append(result)

        return results

    def fetch_restaurant(self, restaurant_id: int) -> Restaurant:
        """Return a restaurant by ID or raise 404."""
        restaurants = self.repo.load_all_restaurants()

        for restaurant in restaurants:
            if restaurant["id"] == restaurant_id:
                return Restaurant(**restaurant)

        raise HTTPException(
                status_code=404,
                detail="Restaurant not found",
            )

    def update_restaurant(self, restaurant_id: int, payload: UpdateRestaurant) -> Restaurant:
        """Updates a restaurant's information"""

        restaurants = self.repo.load_all_restaurants()

        updated_restaurant = UpdateRestaurant(
                        name=payload.name.strip(),
                        hours=payload.hours,
                        phone_number=payload.phone_number.strip(),
                        address=payload.address.strip(),
                        tags=payload.tags
                     )

        for i, restaurant in enumerate(restaurants):
            if restaurant["id"] == restaurant_id:
                ids = {"id" : restaurant_id} | {"user_id" : restaurant["user_id"]}
                restaurant = ids | updated_restaurant.model_dump()
                restaurant = restaurant | {"menu" : restaurants[i]["menu"]}
                restaurants[i] = restaurant
                self.repo.save_all_restaurants(restaurants)
                return Restaurant(**restaurant)

        raise HTTPException(status_code=404, detail=f"Restaurant {restaurant_id} Not Found")

    def delete_restaurant(self, restaurant_id: int) -> None:
        """Deletes restaurant from the data store"""
        restaurants = self.repo.load_all_restaurants()

        for restaurant in restaurants:
            if restaurant["id"] == restaurant_id:
                restaurants.remove(restaurant)
                self.repo.save_all_restaurants(restaurants)
                return

            raise HTTPException(status_code=404, detail=f"Restaurant {restaurant_id} Not Found")

    def get_name_searched_menu_items(self, restaurant: Restaurant, search: str):
        """Get menu items that include a given search term

        Args:
            restaurant: The restaurant object to get the menu from
            search: A string to check if the menu items name includes it

        Returns:
            A list of menuitems including the search term
        """
        menu_items = []
        restaurant = restaurant.model_dump()

        for menu_item in restaurant["menu"]:
            if search.lower() in menu_item["name"].lower():
                menu_items.append(MenuItem(**menu_item))

        return menu_items

    def filter_restaurants_by_tags(self, restaurants: List[RestaurantResult],
                                   tags: List[str] ) -> List[RestaurantResult]:
        """
        Filter a given list of restaurnts based on given list of tags.

        Args:
            restaurants: list of RestaurantResult objects to be filtered
            tags: Specified list of strings to compare to the restaurants tags'

        Returns:
            List of restaurants that have all the tags in the tags List.
        """
        filtered_restaurants = []

        for restaurant in restaurants:
            if set(tags).issubset(restaurant.tags):
                filtered_restaurants.append(restaurant)

        return filtered_restaurants

    def add_item_to_menu(self, restaurant_id: int, payload: MenuItem) -> MenuItem:
        """Add a menu item to a restaurants menu"""

        restaurants = self.repo.load_all_restaurants()

        new_id = str(uuid.uuid7())
        new_menu_item = MenuItem(id=new_id,
                        name=payload.name.strip(),
                        price=payload.price,
                        description=payload.description.strip(),
                        tags=payload.tags
                     )
        for i, restaurant in enumerate(restaurants):
            if restaurant["id"] == restaurant_id:
                for menu_item in restaurant["menu"]:
                    if menu_item["name"] == new_menu_item.name:
                        raise HTTPException(status_code=409, detail="Menu Item Already exists")

                restaurant["menu"].append(new_menu_item.model_dump())
                restaurants[i] = restaurant
                self.repo.save_all_restaurants(restaurants)
                return new_menu_item

        raise HTTPException(status_code=404, detail=f"Restaurant {restaurant_id} Not Found")

    def update_menu_item(self, restaurant_id: int,
                         menu_item_id: str, payload: UpdateMenuItem) -> MenuItem:
        """Update a menu item in a restaurant's menu"""

        restaurants = self.repo.load_all_restaurants()

        updated_menu_item = UpdateMenuItem(
                        name=payload.name.strip(),
                        price=payload.price,
                        description=payload.description.strip(),
                        tags=payload.tags
                     )

        for i, restaurant in enumerate(restaurants):
            if restaurant["id"] == restaurant_id:
                for j, menu_item in enumerate(restaurant["menu"]):
                    if menu_item["id"] == menu_item_id:
                        restaurant["menu"][j]={"id" : menu_item_id} | updated_menu_item.model_dump()
                        restaurants[i] = restaurant
                        self.repo.save_all_restaurants(restaurants)
                        return MenuItem(**restaurant["menu"][j])
                raise HTTPException(status_code=404, detail=f"Menu Item {menu_item_id} Not Found")

        raise HTTPException(status_code=404, detail=f"Restaurant {restaurant_id} Not Found")

    def validate_menu_existence(self, restaurant: Dict[str, Any]) -> None:
        """Ensure restaurant always has at least one menu item."""
        if not restaurant.get("menu") or len(restaurant["menu"]) == 0:
            raise HTTPException(status_code= 400,
                                detail = "Restaurant must have at least one menu item.")

    def delete_menu_item(self, restaurant_id: int, menu_item_id: str) -> None:
        """Deletes menu item from a restaurant's menu"""
        restaurants = self.repo.load_all_restaurants()

        for restaurant in restaurants:
            if restaurant["id"] == restaurant_id:
                for menu_item in restaurant["menu"]:
                    if menu_item["id"] == menu_item_id:
                        restaurant["menu"].remove(menu_item)
                        self.validate_menu_existence(restaurant)
                        self.repo.save_all_restaurants(restaurants)
                        return
                raise HTTPException(status_code=404, detail=f"Menu Item '{menu_item_id}' not found")

        raise HTTPException(status_code=404, detail=f"Restaurant {restaurant_id} Not Found")

#pylint: disable=too-few-public-methods
class IRestaurantRepo(Protocol):
    """Restaurant repository interface"""
    def load_all_restaurants(self) -> List[Dict[str, Any]]:
        """Load all restaurants"""
    def save_all_restaurants(self, restaurant: List[Dict[str, Any]]):
        """Save all resturants"""
