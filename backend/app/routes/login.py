from fastapi import APIRouter , Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.database import get_db
from app.schemas.user import UserLogin , UserLoginResponse
from app.core.security import create_token
import bcrypt

login = APIRouter()

@login.post("/login/", tags=["login"], response_model=UserLoginResponse)
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    if not user.email or not user.password:
        raise HTTPException(status_code=400, detail="all fields are required")
    
    get_user = db.query(User).filter(User.email == user.email).first()
    if not get_user:
        raise HTTPException(status_code=400, detail="the email does not exist")

    if not bcrypt.checkpw(user.password.encode('utf-8'), get_user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="incorrect password")
    
    token = create_token(get_user.id)
    
    return UserLoginResponse(
        message="login successful",
        token= token,
    )