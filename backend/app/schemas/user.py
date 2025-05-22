from pydantic import BaseModel
from typing import Optional, List

class UserBase(BaseModel):
    username: str
    email: str
    phone: str
    password: str

class UserCreate(UserBase):
    confirm_password: str

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

class UserLogin(BaseModel):
    email: str
    password: str

class UserLoginResponse(BaseModel):
    message: str
    token: str

class UserLogout(BaseModel):
    pass






