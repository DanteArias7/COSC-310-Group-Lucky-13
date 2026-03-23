# pylint: disable=too-many-arguments,too-many-positional-arguments
"""Restaurant order management endpoints."""
from typing import List
from fastapi import APIRouter, Depends, Header, HTTPException

from app.repositories.order_repo import OrderRepo
from app.repositories.restaurant_repo import RestaurantRepo
from app.repositories.user_repo import UserRepo
from app.schemas.order import Order
from app.services.authorization_services import AuthorizationServices
from app.services.restaurant_services import RestaurantServices
from app.services.restaurant_order_services import RestaurantOrderServices
from app.routers.order import ORDER_DATA_PATH
from app.routers.restaurant import RESTAURANT_DATA_PATH
from app.routers.user import USER_DATA_PATH

restaurant_order_router = APIRouter(prefix="/restaurants", tags=["restaurant", "orders"])


def create_order_repo():
    """Create order repository instance."""
    return OrderRepo(ORDER_DATA_PATH)


def create_restaurant_repo():
    """Create restaurant repository instance."""
    return RestaurantRepo(RESTAURANT_DATA_PATH)


def create_user_repo():
    """Create user repository instance."""
    return UserRepo(USER_DATA_PATH)


@restaurant_order_router.get("/{restaurant_id}/orders", response_model=List[Order])
def get_restaurant_orders(
    restaurant_id: int,
    order_repo: OrderRepo = Depends(create_order_repo),
    restaurant_repo: RestaurantRepo = Depends(create_restaurant_repo),
    user_repo: UserRepo = Depends(create_user_repo),
    user_id: str = Header(..., alias="user-id")
):
    """Get all orders for a restaurant.

    Rules:
    - User must be the restaurant owner
    - Returns all orders for that restaurant
    """
    # pylint: disable=unused-argument
    # Authorize user
    auth_service = AuthorizationServices(user_repo)
    auth_service.authorize(user_id, "manage_restaurant_orders")

    # Verify restaurant ownership
    restaurant_service = RestaurantServices(restaurant_repo)
    restaurant = restaurant_service.fetch_restaurant(restaurant_id)
    if str(restaurant.user_id) != user_id:
        raise HTTPException(status_code=403, detail="You don't own this restaurant")

    # Get orders
    order_service = RestaurantOrderServices(order_repo)
    return order_service.get_restaurant_orders(restaurant_id)


@restaurant_order_router.get("/{restaurant_id}/orders/{order_id}", response_model=Order)
def get_restaurant_order_detail(
    restaurant_id: int,
    order_id: str,
    order_repo: OrderRepo = Depends(create_order_repo),
    restaurant_repo: RestaurantRepo = Depends(create_restaurant_repo),
    user_repo: UserRepo = Depends(create_user_repo),
    user_id: str = Header(..., alias="user-id")
):
    """Get detailed view of a specific order for restaurant popup."""
    # pylint: disable=unused-argument
    # Authorize user
    auth_service = AuthorizationServices(user_repo)
    auth_service.authorize(user_id, "manage_restaurant_orders")

    # Verify restaurant ownership
    restaurant_service = RestaurantServices(restaurant_repo)
    restaurant = restaurant_service.fetch_restaurant(restaurant_id)
    if str(restaurant.user_id) != user_id:
        raise HTTPException(status_code=403, detail="You don't own this restaurant")

    # Get order
    order_service = RestaurantOrderServices(order_repo)
    return order_service.get_restaurant_order(restaurant_id, order_id)


@restaurant_order_router.post("/orders/{order_id}/accept", response_model=Order)
def accept_order(
    order_id: str,
    order_repo: OrderRepo = Depends(create_order_repo),
    restaurant_repo: RestaurantRepo = Depends(create_restaurant_repo),
    user_repo: UserRepo = Depends(create_user_repo),
    user_id: str = Header(..., alias="user-id")
):
    """Restaurant owner accepts an order.

    Rules:
    - User must be restaurant owner
    - Order must be in 'Paid' status
    - Updates status to 'Accepted_by_restaurant'
    """
    # pylint: disable=unused-argument
    # Authorize user
    auth_service = AuthorizationServices(user_repo)
    auth_service.authorize(user_id, "manage_restaurant_orders")

    # Get order to verify restaurant ownership
    order_repo_instance = order_repo
    orders = order_repo_instance.load_all_orders()
    order = next((o for o in orders if o["id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")

    # Verify restaurant ownership
    restaurant_service = RestaurantServices(restaurant_repo)
    restaurant = restaurant_service.fetch_restaurant(order["restaurant_id"])
    if str(restaurant.user_id) != user_id:
        raise HTTPException(status_code=403, detail="You don't own this restaurant")

    # Process acceptance
    order_service = RestaurantOrderServices(order_repo)
    return order_service.accept_order(order_id, user_id)


@restaurant_order_router.put("/orders/{order_id}/status", response_model=Order)
def update_order_status(
    order_id: str,
    new_status: str,
    order_repo: OrderRepo = Depends(create_order_repo),
    restaurant_repo: RestaurantRepo = Depends(create_restaurant_repo),
    user_repo: UserRepo = Depends(create_user_repo),
    user_id: str = Header(..., alias="user-id")
):
    """Update order status (Preparing → Ready_for_pickup).

    Rules:
    - User must be restaurant owner
    - Valid status transitions only
    """
    # pylint: disable=unused-argument
    # Authorize user
    auth_service = AuthorizationServices(user_repo)
    auth_service.authorize(user_id, "manage_restaurant_orders")

    # Get order to verify restaurant ownership
    order_repo_instance = order_repo
    orders = order_repo_instance.load_all_orders()
    order = next((o for o in orders if o["id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")

    # Verify restaurant ownership
    restaurant_service = RestaurantServices(restaurant_repo)
    restaurant = restaurant_service.fetch_restaurant(order["restaurant_id"])
    if str(restaurant.user_id) != user_id:
        raise HTTPException(status_code=403, detail="You don't own this restaurant")

    # Update status
    order_service = RestaurantOrderServices(order_repo)
    return order_service.update_order_status(order_id, new_status)
