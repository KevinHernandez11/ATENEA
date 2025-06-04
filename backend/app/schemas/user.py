from pydantic import BaseModel
from typing import Optional, List
from app.services.auth_service import get_current_user
import uuid


class UserBase(BaseModel):

    username: str
    email: str
    phone: str
    password: str

class UserCreate(UserBase):
    confirm_password: str

class UserResponse(UserBase):
    id: uuid.UUID
    fk_rol: Optional[int] = None

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None

# class UserDelete(BaseModel):
#     pass

# class UserList(BaseModel):
#     pass

class UserLogout(BaseModel):
    pass






