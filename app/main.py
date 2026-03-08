"""Main application"""
from fastapi import FastAPI
from app.routers.user import user_router
from app.routers.restaurant import restaurant_router
from app.routers.order import order_router
app = FastAPI()

app.include_router(user_router)
app.include_router(restaurant_router)
app.include_router(order_router)
