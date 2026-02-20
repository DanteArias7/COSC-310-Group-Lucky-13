"""Schemas for User Model"""
from pydantic import BaseModel

class User(BaseModel):
    """Schema for a user"""
    id: str
    name: str
    email: str
    phone_number: str
    address: str
    password: str
    role: str

class UserCreate(BaseModel):
    """Schema for creating a user"""
    name: str
    email: str
    phone_number: str
    address: str
    password: str
    role: str
