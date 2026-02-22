"""Main application"""
from fastapi import FastAPI
from app.routers.user import user_router
from app.routers.restaurant import router
app = FastAPI()

app.include_router(user_router)
app.include_router(router)
