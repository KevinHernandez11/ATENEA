from fastapi import APIRouter , Depends, HTTPException
# from app.schemas.user import UserLogin , UserLoginResponse
from app.core.security import create_token
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth_service import authenticate_user
from app.schemas.token import TokenResponse

login = APIRouter()

@login.post("/login/", tags=["login"], response_model=TokenResponse)
async def login_user(form_data:OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_token(user.id)
    
    return TokenResponse(access_token=token, token_type="bearer")
