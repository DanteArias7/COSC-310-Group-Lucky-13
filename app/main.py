"""Main application entry point for the FastAPI backend."""

from fastapi import FastAPI

# Import routers
from app.routers.restaurant import router as restaurant_router

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance.
    """
    application = FastAPI(
        title="COSC 310 Food Delivery Backend"
    )

    # Register routers
    application.include_router(restaurant_router)

    return application


# App instance for tests
app = create_app()
