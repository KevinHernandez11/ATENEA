from fastapi import APIRouter , Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.database import get_db
from app.schemas.user import UserLogin , UserLoginResponse
from app.core.security import create_token
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth_service import authenticate_user
import bcrypt

login = APIRouter()

@login.post("/login/", tags=["login"], response_model=UserLoginResponse)
async def login_user(user: UserLogin, db: Session = Depends(get_db), form_data:OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_token(user.id)
    
    return UserLoginResponse(
        message="login successful",
        token= token,
    )