"""API Endpoints for Order functionality"""
from pathlib import Path
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Header
from app.repositories.order_repo import OrderRepo
from app.repositories.restaurant_repo import RestaurantRepo
from app.repositories.user_repo import UserRepo
from app.routers.restaurant import RESTAURANT_DATA_PATH
from app.routers.user import USER_DATA_PATH
from app.schemas.cart import Cart
from app.schemas.order import Order
from app.services.authorization_services import AuthorizationServices
from app.services.order_services import OrderServices
from app.schemas.payment import Payment, PaymentResult
from app.services.restaurant_services import RestaurantServices

ORDER_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "orders.csv"

order_router = APIRouter(prefix="/orders",
                         tags=["order"])

def create_order_repo():
    """"Initialize repo object with data path to user data store

    Returns:
            UserRepo object with the order data path attribute"""
    return OrderRepo(ORDER_DATA_PATH)

def create_restaurant_repo():
    """"Initialize repo object with data path to user data store

    Returns:
            UserRepo object with the order data path attribute"""
    return RestaurantRepo(RESTAURANT_DATA_PATH)

def create_user_repo():
    """"Initialize repo object with data path to user data store

    Returns:
            UserRepo object with the order data path attribute"""
    return UserRepo(USER_DATA_PATH)

@order_router.post("", response_model=Order, status_code=201)
def add_order(payload: Cart,
                 order_repo: OrderRepo = Depends(create_order_repo),
                 restaurant_repo: RestaurantRepo = Depends(create_restaurant_repo),
                 user_repo: UserRepo = Depends(create_user_repo),
                 user_id: str = Header(...,alias="user-id")):
    """Adds a user created order to the data store

    Rules: User must have customer role, Restayrant must be open

    Args:
        payload: Cart object to get information from to create cart object,
        order_repo: The order repo object to allow order_service to access order data store,
        user_repo: The user repo object to allow order_service to access user data store,
        user_id: header sent with request indicating current user

    Returns: New order object

    Raises:
        409 Error if restaurant is closed
        404 Error if requesting user is not found
        403 Error if requesting user does not have the correct access or role
        """
    authorization_service = AuthorizationServices(user_repo)
    restaurant_service = RestaurantServices(restaurant_repo)
    order_service = OrderServices(order_repo, restaurant_service)
    authorization_service.authorize(user_id, "create_order")
    authorization_service.authorize_access(user_id, payload.user_id)
    restaurant_service.validate_restaurant_is_open(payload.restaurant_id)
    return order_service.place_order(payload)

@order_router.get("", response_model=List[Order], status_code=200)
def get_all_orders_for_a_user(order_repo: OrderRepo = Depends(create_order_repo),
                 user_repo: UserRepo = Depends(create_user_repo),
                 user_id: str = Header(...,alias="user-id")):
    """Gets all the previous and current orders for a given user.

    Rules: User must have customer role

    Args:
    order_repo: The order repo object to allow order_service to access order data store,
    user_repo: The user repo object to allow order_service to access user data store,
    user_id: header sent with request indicating current user

    Returns: List of order objects pertaining to the given user"""
    order_service = OrderServices(order_repo)
    authorization_service = AuthorizationServices(user_repo)
    authorization_service.authorize(user_id, "view_own_orders")
    return order_service.get_orders_by_user_id(user_id)

#pylint: disable=too-many-arguments
#pylint: disable=too-many-positional-arguments
@order_router.post("/{order_id}/simulate-payment", response_model=PaymentResult, status_code=200)
def simulate_payment(order_id: str,
                     payload: Payment,
                     order_repo: OrderRepo = Depends(create_order_repo),
                     restaurant_repo: RestaurantRepo = Depends(create_restaurant_repo),
                     user_repo: UserRepo = Depends(create_user_repo),
                     user_id: str = Header(..., alias="user-id")):
    """Simulates payment processing for an order

    Rules: User must have customer role

    Args:
        order_id: ID of order to process payment for
        payload: Payment object containing the payment details to validate
        order_repo: Order repository instance
        user_repo: User repository instance
        user_id: header sent with request indicating current user

    Returns:
        The payment result of the simulated payment process
    """

    restaurant_service = RestaurantServices(restaurant_repo)
    order_service = OrderServices(order_repo , restaurant_service)
    authorization_service = AuthorizationServices(user_repo)
    authorization_service.authorize(user_id, "make_payment")
    authorization_service.authorize_access(user_id, payload.user_id)
    return order_service.simulate_payment(order_id, payload)

@order_router.get("/available", response_model=List[Order], status_code=200)
def get_all_available_delivery_orders(
        order_repo: OrderRepo = Depends(create_order_repo),
        user_repo: UserRepo = Depends(create_user_repo),
        user_id: str = Header(..., alias="user-id")):
    """Gets all orders available for delivery drivers to pick up.

    Rules:
    - user must have delivery_driver role

    Args:
    order_repo: Order repository
    user_repo: User repository
    user_id: current user

    Returns: List of available Order objects

    Raises:
        403 if user does not have delivery_driver role
    """
    order_service = OrderServices(order_repo)
    authorization_service = AuthorizationServices(user_repo)
    authorization_service.authorize(user_id, "view_available_deliveries")
    return order_service.get_all_available_delivery_orders()

@order_router.get("/available", response_model=List[Order], status_code=200)
def get_available_orders(
    order_repo: OrderRepo = Depends(create_order_repo),
    user_repo: UserRepo = Depends(create_user_repo),
    user_id: str = Header(..., alias="user-id")
):
    """Get all orders ready for pickup that are not yet assigned.

    Rules: User must have driver role

    Returns orders with status 'Ready_for_pickup' and no assigned driver
    """
    authorization_service = AuthorizationServices(user_repo)
    authorization_service.authorize(user_id, "view_available_orders")

    order_service = OrderServices(order_repo)
    return order_service.get_available_orders()


@order_router.post("/{order_id}/accept-driver", response_model=Order, status_code=200)
def accept_delivery(
    order_id: str,
    order_repo: OrderRepo = Depends(create_order_repo),
    user_repo: UserRepo = Depends(create_user_repo),
    user_id: str = Header(..., alias="user-id")
):
    """Driver accepts an order to deliver.

    Rules:
    - User must have driver role
    - Order must be in 'Ready_for_pickup' status
    - Order must not have an assigned driver
    """
    authorization_service = AuthorizationServices(user_repo)
    authorization_service.authorize(user_id, "view_available_orders")

    order_service = OrderServices(order_repo)
    return order_service.accept_delivery(order_id, user_id)

@order_router.put("/{order_id}/driver-status", response_model=Order, status_code=200)
def update_delivery_status(
    order_id: str,
    new_status: str,
    order_repo: OrderRepo = Depends(create_order_repo),
    user_repo: UserRepo = Depends(create_user_repo),
    restaurant_repo: RestaurantRepo = Depends(create_restaurant_repo), # pylint: disable=unused-argument
    user_id: str = Header(..., alias="user-id")
):
    """Driver updates delivery status.

    Rules:
    - User must have driver role
    - Order must be assigned to this driver
    - Valid transitions: 'Ready_for_pickup' → 'In_transit' → 'Complete'
    - Customer receives notification on each status update
    """
    # Authorize user role
    auth_service = AuthorizationServices(user_repo)
    auth_service.authorize(user_id, "view_available_orders")

    order_service = OrderServices(order_repo)

    orders = order_repo.load_all_orders()
    order_dict = next((o for o in orders if o["id"] == order_id), None)
    if not order_dict:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")

    auth_service.authorize_access(user_id, order_dict["assigned_driver_id"])

    return order_service.update_delivery_status(order_id, user_id, new_status)
