"""Schemas for User Model"""
from sqlmodel import SQLModel, Field
from pydantic import BaseModel

class User(SQLModel, table = True):
    """Schema for a user"""
    id: str = Field(primary_key = True)
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
    