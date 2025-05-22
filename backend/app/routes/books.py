from fastapi import APIRouter , Depends, HTTPException

books = APIRouter()

@books.get("/books/", tags=["books"])
async def read_books():
    return {"message": "List of books"}