from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.core.database import Supabase
from app.schemas.user import user

router = APIRouter()

@router.post("/register/", tags=["register"])
async def read_users(user: user):
    if user.username == "":
        return JSONResponse(status_code=400, content={"message": "Username is required"})
    return "User registered successfully"
        
