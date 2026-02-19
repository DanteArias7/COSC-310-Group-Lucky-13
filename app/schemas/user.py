from sqlmodel import SQLModel, Field
from pydantic import BaseModel


class User(SQLModel, table = True):
    id: str = Field(primary_key = True)
    name: str
    email: str
    phone_number: str
    address: str
    password: str
    role: str

class UserCreate(BaseModel):
    name: str
    email: str
    phone_number: str
    address: str
    password: str
    role: str 