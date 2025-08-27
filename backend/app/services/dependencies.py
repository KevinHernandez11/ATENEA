from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from app.core.database import get_db 
from fastapi import HTTPException , Depends
from passlib.context import CryptContext
from app.models.user import User 
from app.models.book import Books
import datetime
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
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=JWTService.EXPEDTION_TIME)
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
    def auth_rol_user_books(User: User) -> User:
        if not User:
            raise HTTPException(status_code=401, detail="Not authenticated")
        user = User

        if not user.rol:
            raise HTTPException(status_code=403, detail="Access forbidden: No role assigned")

        roles = [
            "Admin",
            "User",
            "SuperUser"
        ]

        if not user:
            raise HTTPException(status_code=401, detail="Not authenticated")
        if user.rol.name in roles:
            return user
        raise HTTPException(status_code=403, detail="Access forbidden")
    

