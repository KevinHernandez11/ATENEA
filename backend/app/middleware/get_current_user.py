from fastapi import Request, HTTPException
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.core.database import SessionLocal
from app.models.user import User
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGHORITHM = os.getenv("ALGHORITHM")


def get_current_user(token: str):
    db: Session = SessionLocal()
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGHORITHM)
        username: str = payload.get("username")
        if username is None:
            return HTTPException (status_code=401, detail="Could not validate credentials")
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            return HTTPException (status_code=401, detail="Could not validate credentials")
        return user
    except JWTError:
        return HTTPException (status_code=401, detail="Could not validate credentials")
    finally:
        db.close()
    
    

