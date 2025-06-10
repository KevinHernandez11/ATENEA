from fastapi import APIRouter , Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User, Rol
from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.dependencies import HashService
from fastapi.security import OAuth2PasswordRequestForm

register = APIRouter()

@register.post("/register/", tags=["register"], response_model=UserResponse, )
async def read_users(form_data:OAuth2PasswordRequestForm = Depends(UserCreate), db: Session = Depends(get_db)):

    if not all([form_data.username, form_data.email, form_data.password, form_data.confirm_password]):
        raise HTTPException(status_code=400, detail="all fields are required")
    
    if form_data.password != form_data.confirm_password:
        raise HTTPException(status_code=400, detail="passwords do not match")
    
    get_user = db.query(User).filter(User.username == form_data.username).first()
    if get_user:
        raise HTTPException(status_code=400, detail="the username already exists")
    
    get_email = db.query(User).filter(User.email == form_data.email).first()
    if get_email:
        raise HTTPException(status_code=400, detail="the email already exists")
    
    get_phone = db.query(User).filter(User.phone == form_data.phone).first()
    if get_phone:
        raise HTTPException(status_code=400, detail="the phone already exists")
    
    hashed_password = HashService.get_password_hash(form_data.password)

    get_rol = db.query(Rol).filter(Rol.name == "User").first()

    data_user = User(  
        username=form_data.username,
        email=form_data.email,
        phone=form_data.phone,
        hashed_password=hashed_password,
        fk_rol = get_rol.id
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
        fk_rol=data_user.rol.name
    )
    

        
