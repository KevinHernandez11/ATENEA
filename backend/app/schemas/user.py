from pydantic import BaseModel
from typing import Optional, List

class UserBase(BaseModel):
    username: str
    email: str
    phone: str
    password: str

class UserCreate(UserBase):
    pass





