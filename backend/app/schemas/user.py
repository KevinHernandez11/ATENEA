from pydantic import BaseModel
from typing import Optional, List

class UserBase(BaseModel):
    username: str
    email: str
    phone: str
    password: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    fk_rol: Optional[int] = None

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None

class UserDelete(BaseModel):
    id: int

class UserList(BaseModel):
    pass





