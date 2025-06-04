from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException , Depends
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.services.dependencies import get_current_user
from app.models.user import User

import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class HashService():
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)


class JWTService():
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGHORITHM = os.getenv("ALGHORITHM")
    EXPEDTION_TIME = int(os.getenv("EXPEDTION_TIME", 24))
    
    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, JWTService.SECRET_KEY, JWTService.ALGHORITHM)

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, JWTService.SECRET_KEY, JWTService.ALGHORITHM)
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        

class AuthService():

    @staticmethod
    def auth_rol_user(user: User = Depends(get_current_user)):

        roles = [
            "Admin",
            "User"
            "SuperUser"
            "Guest"
        ]


        if not user:
            raise HTTPException(status_code=401, detail="Not authenticated")
        if user.fk_rol != roles[0] or user.fk_rol != roles[1]:
            raise HTTPException(status_code=403, detail="Access forbidden: Admins only")
        return user

