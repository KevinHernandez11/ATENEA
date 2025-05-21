from fastapi import APIRouter , Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.models.user import User
from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()

@router.post("/register/", tags=["register"], response_model=UserResponse, )
async def read_users(user: UserCreate, db: Session = Depends(get_db)):

    if not user.username or not user.email or not user.password:
        raise HTTPException(status_code=400, detail="Faltan datos del usuario")

    
    data_user = User(
        fk_rol=None,  
        username=user.username,
        email=user.email,
        phone=user.phone,
        hashed_password=user.password,
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
    

        
