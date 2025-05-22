from fastapi import APIRouter , Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.models.user import User
from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse
import bcrypt

home = APIRouter()
@home.get("/", tags=["home"])
async def read_users():
    return JSONResponse(content={"message": "Welcome to the ATENEA API"}, status_code=200)
 