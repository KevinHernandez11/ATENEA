from fastapi import APIRouter , Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse
import bcrypt

register = APIRouter()

@register.post("/register/", tags=["register"], response_model=UserResponse, )
async def read_users(user: UserCreate, db: Session = Depends(get_db)):

    if not user.username or not user.email or not user.password or not user.confirm_password:
        raise HTTPException(status_code=400, detail="all fields are required")
    
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="passwords do not match")
    
    get_user = db.query(User).filter(User.username == user.username).first()
    if get_user:
        raise HTTPException(status_code=400, detail="the username already exists")
    
    get_email = db.query(User).filter(User.email == user.email).first()
    if get_email:
        raise HTTPException(status_code=400, detail="tthe email already exists")
    
    get_phone = db.query(User).filter(User.phone == user.phone).first()
    if get_phone:
        raise HTTPException(status_code=400, detail="the phone already exists")
    
    

    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    
    data_user = User(
        fk_rol=None,  
        username=user.username,
        email=user.email,
        phone=user.phone,
        hashed_password=hashed_password,
    )

    db.add(data_user)
    db.commit()
    db.refresh(data_user)

    return UserResponse(
        id=data_user.id,
        username=data_user.username,
        email=data_user.email,
        phone=data_user.phone,
        password=data_user.hashed_password,
        fk_rol=data_user.fk_rol,
    )
    

        
