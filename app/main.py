"""Main application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from app.routers.user import user_router
from app.routers.restaurant import restaurant_router
from app.routers.order import order_router
from app.routers.notification_router import notification_router
from app.routers.login import login_router
from app.routers.favorite_router import favorite_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(restaurant_router)
app.include_router(order_router)
app.include_router(notification_router)
app.include_router(login_router)
app.include_router(favorite_router)

add_pagination(app)
