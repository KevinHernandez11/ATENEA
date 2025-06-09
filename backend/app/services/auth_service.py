from fastapi import Request, HTTPException
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.core.database import SessionLocal
from app.models.user import User
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer
from fastapi import Depends
from datetime import datetime, timedelta
from app.core.database import get_db
from app.services.dependencies import JWTService, HashService
from typing import Annotated
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGHORITHM = os.getenv("ALGHORITHM")
EXPEDTION_TIME = int(os.getenv("EXPEDTION_TIME", 24))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login/")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    try:
        payload = JWTService.decode_token(token)
        user_id: str = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials") 
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="error")
    
# Función para autenticar usuario
def authenticate_user(email: str, password: str):
    user = SessionLocal().query(User).filter(User.email == email).first()
    if not user or not HashService.verify_password(password, user.hashed_password):
        return HTTPException(status_code=401, detail="Invalid email or password")
    return user

