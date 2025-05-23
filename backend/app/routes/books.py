from fastapi import APIRouter , Depends, HTTPException
from app.middleware.get_current_user import get_current_user

books = APIRouter()

@books.get("/books/", tags=["books"])
async def read_books(user: str = Depends(get_current_user)):
    return {"message": "Hello, this is the books route", "user": user.username}


#fastapi




