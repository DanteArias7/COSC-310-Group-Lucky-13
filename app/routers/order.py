"""API Endpoints for Order functionality"""
from pathlib import Path
from typing import List
from fastapi import APIRouter, Depends, Header
from app.repositories.order_repo import OrderRepo
from app.repositories.user_repo import UserRepo
from app.routers.user import USER_DATA_PATH
from app.schemas.cart import Cart
from app.schemas.order import Order
from app.services.authorization_services import AuthorizationServices
from app.services.order_services import OrderServices
from app.schemas.payment import Payment, PaymentResult

ORDER_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "orders.csv"

order_router = APIRouter(prefix="/orders",
                         tags=["order"])

def create_order_repo():
    """"Initialize repo object with data path to user data store

    Returns:
            UserRepo object with the order data path attribute"""
    return OrderRepo(ORDER_DATA_PATH)

def create_user_repo():
    """"Initialize repo object with data path to user data store

    Returns:
            UserRepo object with the order data path attribute"""
    return UserRepo(USER_DATA_PATH)

@order_router.post("", response_model=Order, status_code=201)
def add_order(payload: Cart,
                 order_repo: OrderRepo = Depends(create_order_repo),
                 user_repo: UserRepo = Depends(create_user_repo),
                 user_id: str = Header(...,calias="user-id")):
    """Adds a user created order to the data store

    Rules: User must have customer role

    Args:
    payload: Cart object to get information from to create cart object,
    order_repo: The order repo object to allow order_service to access order data store,
    user_repo: The user repo object to allow order_service to access user data store,
    user_id: header sent with request indicating current user

    Returns: New order object"""
    order_service = OrderServices(order_repo)
    authorization_service = AuthorizationServices(user_repo)
    authorization_service.authorize(user_id, "create_order")
    authorization_service.authorize_access(user_id, payload.user_id)
    return order_service.place_order(payload)

@order_router.get("", response_model=List[Order], status_code=200)
def get_all_orders_for_a_user(order_repo: OrderRepo = Depends(create_order_repo),
                 user_repo: UserRepo = Depends(create_user_repo),
                 user_id: str = Header(...,calias="user-id")):
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

@order_router.post("/{order_id}/simulate-payment", response_model=PaymentResult, status_code=200)
def simulate_payment(order_id: str,
                     payload: Payment,
                     order_repo: OrderRepo = Depends(create_order_repo),
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

    order_service = OrderServices(order_repo)
    authorization_service = AuthorizationServices(user_repo)
    authorization_service.authorize(user_id, "make_payment")
    return order_service.simulate_payment(order_id, payload)
