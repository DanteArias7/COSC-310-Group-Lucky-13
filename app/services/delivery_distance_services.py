"""Service for calculating delivery distances using the Google Maps Routes API."""
import os
import httpx
from fastapi import HTTPException


GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
GOOGLE_ROUTES_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"

# pylint: disable=too-few-public-methods
class DeliveryDistanceServices:
    """Handles driving distance calculations between two addresses via Google Maps."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_distance_km(self, origin_address: str, destination_address: str) -> float:
        """
        Uses Google Maps API computeRoutes to get driving distance in km between two addresses.

        Args:
            origin_address: starting address (restaurant)
            destination_address: delivery address (customer)

        Returns:
            distance in km as a float

        Raises:
            HTTPException 503 if the Maps API call fails
        """
        payload = {
            "origin": {"address": origin_address},
            "destination": {"address": destination_address},
            "travelMode": "DRIVE",
        }
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": "routes.distanceMeters",
        }

        response = httpx.post(GOOGLE_ROUTES_URL, json=payload, headers=headers)

        if response.status_code != 200 or not response.json().get("routes"):
            raise HTTPException(
                status_code=503,
                detail="Unable to calculate delivery distance. Please check addresses."
            )

        distance_meters = response.json()["routes"][0]["distanceMeters"]
        return round(distance_meters / 1000, 0)
