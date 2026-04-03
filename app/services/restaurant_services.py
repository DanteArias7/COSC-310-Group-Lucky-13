"""Service layer for restaurant business logic."""

from datetime import date, datetime, time
import re
from typing import Any, Dict, List, Protocol
import uuid
from fastapi import HTTPException
from app.schemas.menu import CreateMenuItem, MenuItem, UpdateMenuItem
from app.schemas.rating import CreateRating, Rating
from app.schemas.restaurant import RestaurantResult, Restaurant, RestaurantCreate, UpdateRestaurant

class RestaurantServices:
    """Restaurant service methods"""
    def __init__(self, repo: IRestaurantRepo):
        """Initialize instance with repo object"""
        self.repo = repo

    def create_new_restaurant(self, user_id: str, restaurant: RestaurantCreate) -> Restaurant:
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

        restaurants = self.repo.load_all_restaurants()
        new_menu = []

        new_restaurant_id = restaurants[-1]["id"] + 1

        for menu_item in restaurant.menu:
            menu_item_id = str(uuid.uuid4())
            new_menu.append(MenuItem(id=menu_item_id, **menu_item.model_dump()))

        restaurant = Restaurant(
            id=new_restaurant_id,
            user_id=user_id,
            name=restaurant.name,
            hours=restaurant.hours,
            phone_number=restaurant.phone_number,
            address=restaurant.address,
            tags=restaurant.tags,
            menu=new_menu,
            average_rating= None,
            ratings = []
        )

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
                        tags=restaurant["tags"],
                        average_rating=restaurant["average_rating"]
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
                                  tags=restaurant["tags"],
                        average_rating=restaurant["average_rating"])
                results.append(result)

        return results

    def fetch_restaurant(self, restaurant_id: int) -> Restaurant:
        """Return a restaurant that matches a given ID

        Args:
            restaurant_id: ID of the restaurant being fetched

        Returns:
            A restaurant object that matches the given id

        Raises:
            A 404 HTTPException if the restaurant is not found"""
        restaurants = self.repo.load_all_restaurants()

        for restaurant in restaurants:
            if restaurant["id"] == restaurant_id:
                return Restaurant(**restaurant)

        raise HTTPException(
                status_code=404,
                detail="Restaurant not found",
            )

    def update_restaurant(self, restaurant_id: int,
                          updated_restaurant: UpdateRestaurant) -> Restaurant:
        """Updates a restaurant's identifying information

        Args:
            restaurant_id: The ID of the restaurant being updated
            updated_restaurant: The UpdateRestaurant object containing
            the new info

        Returns:
            The updated Restaurant object

        Raises:
            A 404 HTTPException if the restaurant is not found"""

        restaurants = self.repo.load_all_restaurants()

        for i, restaurant in enumerate(restaurants):
            if restaurant["id"] == restaurant_id:
                ids = {"id" : restaurant_id} | {"user_id" : restaurant["user_id"]}
                menu = restaurant["menu"]
                average_rating = {"average_rating": restaurant["average_rating"]}
                ratings = {"ratings": restaurant["ratings"]}

                restaurant = ids | updated_restaurant.model_dump()
                restaurant = restaurant | {"menu" : menu}
                restaurant = restaurant | average_rating | ratings

                restaurants[i] = restaurant
                self.repo.save_all_restaurants(restaurants)
                return Restaurant(**restaurant)

        raise HTTPException(status_code=404, detail=f"Restaurant {restaurant_id} Not Found")

    def delete_restaurant(self, restaurant_id: int) -> None:
        """Deletes a restaurant that matches a given ID

        Args:
            restaurant_id: ID of the restaurant being deleted

        Returns:
            Nothing

        Raises:
            A 404 HTTPException if the restaurant is not found"""
        restaurants = self.repo.load_all_restaurants()

        for restaurant in restaurants:
            if restaurant["id"] == restaurant_id:
                restaurants.remove(restaurant)
                self.repo.save_all_restaurants(restaurants)
                return

        raise HTTPException(status_code=404, detail=f"Restaurant {restaurant_id} Not Found")

    def validate_restaurant_is_open(self, restaurant_id: int) -> bool:
        """Validates that a given restaurant is currently open.

        Args:
            restaurant_id: The ID of the restaurant being validated

        Returns:
            True if the restaurant is open

        Raises: 409 HTTPException if restaurant is closed.
        """
        restaurant = self.fetch_restaurant(restaurant_id)
        times = self.get_current_operating_times(restaurant)
        current_time = datetime.now().time()

        open_time = times["open"]
        closed_time = times["closed"]

        if open_time <= closed_time:
            if open_time <= current_time <= closed_time:
                return True

        else:
            if(open_time <= current_time or current_time <= closed_time):
                return True

        raise HTTPException(status_code=409,
                            detail="Restaurant is currently closed")

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

    def filter_menu_items_by_tags(self, menu_items: List[MenuItem],
                                   tags: List[str]) -> List[MenuItem]:
        """
        Filter a given list of menuItems based on given list of tags.

        Args:
            menu_items: list of MenuItem objects to be filtered
            tags: List of tags to match to the menu_items

        Returns:
            List of menuItems that have all the specified tags"""

        filtered_menu_items = []

        for i, tag in enumerate(tags):
            tags[i] = tag.lower()

        for menu_item in menu_items:
            menu_item_tags = menu_item.tags
            for i, menu_item_tag in enumerate(menu_item_tags):
                menu_item_tags[i] = menu_item_tag.lower()

            if set(tags).issubset(menu_item_tags):
                filtered_menu_items.append(menu_item)

        return filtered_menu_items

    def filter_menu_items_by_price(self, menu_items: List[MenuItem],
                                   price_max: float, price_min: float)-> List[MenuItem]:
        """
        Filter a given list of menuItems based on a price range.

        Args:
            menu_items: list of MenuItem objects to be filtered
            max: Maximum range of the price
            min: Minimum wage of the price

        Returns:
            List of menuItems that have a price within the given range
        """
        filtered_menu_items = []

        for menu_item in menu_items:
            if menu_item.price < price_max and menu_item.price > price_min:
                filtered_menu_items.append(menu_item)

        return filtered_menu_items

    def filter_restaurants_by_tags(self, restaurants: List[RestaurantResult],
                                   tags: List[str] ) -> List[RestaurantResult]:
        """
        Filter a given list of restaurants based on given list of tags.

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

    def filter_closed_restaurants(self,
                                  restaurants: List[RestaurantResult]) -> List[RestaurantResult]:
        """
        Filter a given list of restaurants based on if they are currently open or not.

        Args:
            restaurants: list of RestaurantResult objects to be filtered

        Returns:
            List of restaurants that are currently open
        """
        open_restaurants = []

        current_time = datetime.now().time()

        for restaurant in restaurants:
            times = self.get_current_operating_times(restaurant)
            open_time = times["open"]
            closed_time = times["closed"]

            if open_time <= closed_time:
                if open_time <= current_time <= closed_time:
                    open_restaurants.append(restaurant)
            else:
                if(open_time <= current_time or current_time <= closed_time):
                    open_restaurants.append(restaurant)

        return open_restaurants

    def get_current_operating_times(self, restaurant: RestaurantResult | Restaurant):
        """
        Determine a given restaurants open and closing times.

        Args:
            restaurants: Either a restaurantResult or a Restaurant object

        Returns:
            A dict of the open and closing times as time objects, of the
            given Restaurant/RestaurantResult object
        """

        today = date.today().strftime("%A")

        if isinstance(restaurant, RestaurantResult):
            times = re.split(r"[:-]", restaurant.todays_hours)
        else:
            times = re.split(r"[:-]", restaurant.hours[today])

        open_hour = int(times[0])
        open_minute = int(times[1])
        closed_hour = int(times[2])
        closed_minute = int(times[3])
        open_time = time(open_hour, open_minute)
        closed_time = time(closed_hour, closed_minute)

        times = {"open":open_time, "closed":closed_time}
        return times

    def add_item_to_menu(self, restaurant_id: int, new_menu_item: CreateMenuItem) -> MenuItem:
        """Add a menu item to a restaurants menu

        Args:
            restaurant_id: The ID of the restaurant having a menu_item added
            to its menu.
            menu_item: A MenuItem Object containing the information of the
            MenuItem

        Returns:
            The new MenuItem object

        Raises:
            A 409 HTTPException if menu item has the same name already
            A 404 HTTPException if the restaurant is not found
            """

        restaurants = self.repo.load_all_restaurants()

        new_id = str(uuid.uuid7())
        created_menu_item = MenuItem(id=new_id,
                        name=new_menu_item.name.strip(),
                        price=new_menu_item.price,
                        description=new_menu_item.description.strip(),
                        tags=new_menu_item.tags
                     )

        for i, restaurant in enumerate(restaurants):
            if restaurant["id"] == restaurant_id:
                for menu_item in restaurant["menu"]:
                    if menu_item["name"] == created_menu_item.name:
                        raise HTTPException(status_code=409, detail="Menu Item Already exists")

                restaurant["menu"].append(created_menu_item.model_dump())
                restaurants[i] = restaurant
                self.repo.save_all_restaurants(restaurants)
                return created_menu_item

        raise HTTPException(status_code=404, detail=f"Restaurant {restaurant_id} Not Found")

    def update_menu_item(self, restaurant_id: int,
                         menu_item_id: str, updated_menu_item: UpdateMenuItem,
                         item_status: str | None = None) -> MenuItem:
        """Update a menu item in a restaurant's menu

        Args:
            restaurant_id: The ID of the Restaurant that has the menu
            item
            menu_item_id: The ID of the MenuItem being updated
            updated_menu_item: An UpdateMenuItem object that contains
            the updated information
            item_status: An optional argument, the new status of the
            MenuItem

        Returns:
            The updated MenuItem object

        Raise:
            A 404 HTTPException if the restaurant or menu item are not found
        """

        restaurants = self.repo.load_all_restaurants()

        for restaurant in restaurants:
            if restaurant["id"] == restaurant_id:
                for j, item in enumerate(restaurant["menu"]):
                    if item["id"] == menu_item_id:
                        menu_item_id = {"id" : menu_item_id}
                        current_status = {"status" : item["status"]}
                        new_status = {"status" : item_status}

                        restaurant["menu"][j] = menu_item_id | updated_menu_item.model_dump()

                        if item_status is None:
                            restaurant["menu"][j] = restaurant["menu"][j] | current_status
                        else:
                            restaurant["menu"][j] = restaurant["menu"][j] | new_status

                        self.repo.save_all_restaurants(restaurants)
                        return MenuItem(**restaurant["menu"][j])

                raise HTTPException(status_code=404, detail=f"Menu Item {menu_item_id} Not Found")

        raise HTTPException(status_code=404, detail=f"Restaurant {restaurant_id} Not Found")

    def validate_menu_item_is_available(self, restaurant_id: int, menu_item_id: str) -> bool:
        """Validates that a given menu_item is currently available.

        Args:
            menu_item_id: The ID of the menu_item being validated

        Returns:
            True if the MenuItem is available

        Raises:
            400 HTTPException if menuItem is not available.
            404 HTTPException if MenuItem is not found.
        """
        restaurant = self.fetch_restaurant(restaurant_id)

        for menu_item in restaurant.menu:
            if menu_item.id == menu_item_id:
                if menu_item.status != "Available":
                    raise HTTPException(status_code=400,
                                        detail=f"{menu_item.name} Is Unavailable")
                return True

        raise HTTPException(status_code=404,
                            detail=f"Menu Item {menu_item_id} Not Found.")

    def validate_menu_existence(self, restaurant: Dict[str, Any]) -> None:
        """
        A validation check to ensure a restaurant always has at least one menu item.

        Args:
            restaurant: Dict representing a restaurant Object

        Returns:
            Nothing

        Raises:
            A 400 HTTPException if the restaurant is not found
        """

        if not restaurant.get("menu"):
            raise HTTPException(status_code=400,
                                detail="Restaurant must have at least one menu item.")

    def delete_menu_item(self, restaurant_id: int, menu_item_id: str) -> None:
        """Deletes a menu_item from a restaurants menu that matches a given ID

        Args:
            restaurant_id: ID of the restaurant containing the menu_item
            menu_item_id: ID of the menu_item being deleted

        Returns:
            Nothing

        Raises:
            A 404 HTTPException if the restaurant or the MenuItem is not found
        """
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

    def add_rating(self, restaurant_id: int, rating: CreateRating) -> Rating:
        """Adds a rating to a restaurant and updates the restaurant's average rating

        Args:
            restaurant_id: The ID of the restaurant having a review added
            review: A CreateReview object containg the information about the review

        Returns:
            The Updated List of the Restaurant's Ratings """

        new_id = str(uuid.uuid4())

        new_rating = Rating(id=new_id,
                            customer_id=rating.customer_id,
                            rating=rating.rating,
                            review=rating.review)

        restaurants = self.repo.load_all_restaurants()

        for restaurant in restaurants:
            if restaurant["id"] == restaurant_id:
                restaurant["ratings"].append(new_rating.model_dump())
                restaurant["average_rating"] = self._calculate_average_rating(restaurant["ratings"])
                self.repo.save_all_restaurants(restaurants)
                return new_rating

        raise HTTPException(status_code=404, detail=f"Restaurant {restaurant_id} Not Found")

    def _calculate_average_rating(self, ratings: List[Dict]):
        """Calcualted the average rating of a restaurant's ratings

        Args:
            ratings: A list of ratings in dict form

        Returns:
            The average of all the ratings as a float
        """

        rating_sum = 0
        count = 0

        for rating in ratings:
            rating_sum += rating["rating"]
            count += 1

        return round(sum/count, 2)


#pylint: disable=too-few-public-methods
class IRestaurantRepo(Protocol):
    """Restaurant repository interface"""
    def load_all_restaurants(self) -> List[Dict[str, Any]]:
        """Load all restaurants from the data store"""
    def save_all_restaurants(self, restaurant: List[Dict[str, Any]]):
        """Save all resturants to the data store"""
