"""Rating Schemas"""
from pydantic import BaseModel, Field

class Rating(BaseModel):
    """Resturant Rating entity"""
    id: str
    customer_id: str
    rating: float = Field(ge=0.5, le=5.0, multiple_of=0.5)
    review: str
