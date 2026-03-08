"""API Endpoints for Order functionality"""
from pathlib import Path
from fastapi import APIRouter, Depends, Header
from app.repositories.order_repo import OrderRepo
from app.repositories.user_repo import UserRepo
from app.routers.user import USER_DATA_PATH
from app.schemas.cart import Cart
from app.schemas.order import Order
from app.services.authorization_services import AuthorizationServices
from app.services.order_services import OrderServices

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
    return order_service.place_order(payload)
