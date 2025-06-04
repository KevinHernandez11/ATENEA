from fastapi import APIRouter , Depends, HTTPException
from app.services.auth_service import get_current_user
from app.schemas.book import BookResponse , BookCreate
from sqlalchemy.orm import Session
from app.models.book import Books
from app.core.database import get_db 
from app.services.auth_service import get_current_user
from app.models.user import User

books = APIRouter()

@books.get("/books/", tags=["books"])
async def read_books(user: User = Depends(get_current_user)):
    print(user.username)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if user.fk_rol != 1:
        raise HTTPException(status_code=403, detail="Access forbidden: Admins only")



@books.post("/books/", tags=["books"], response_model=BookResponse)
async def create_book(book: BookCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if user.fk_rol != 1:
        raise HTTPException(status_code=403, detail="Access forbidden: Admins only")
    
    new_book = Books(
        name=book.name,
        author=book.author,
        description=book.description
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    
    return BookResponse(
        name=book.name,
        author=book.author,
        description=book.description
    )

@books.get("/{book_id}")
async def get_book(book_id: int, user: User = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if user.fk_rol != 1:
        raise HTTPException(status_code=403, detail="Access forbidden: Admins only")

    return {"book_id": book_id, "title": "Sample Book", "author": "Author Name"}

# @books.put("/{book_id}", tags=["books"], response_model=BookResponse)
# async def update_book(book_id: int, book: BookCreate, user: str = Depends(get_current_user)):
#     if not user:
#         raise HTTPException(status_code=401, detail="Not authenticated")
#     if user.get("fk_rol") != 1:
#         raise HTTPException(status_code=403, detail="Access forbidden: Admins only")

#     return BookResponse(
#         title=book.title,
#         author=book.author,
#         description=book.description
#     )

# @books.delete("/{book_id}", tags=["books"])
# async def delete_book(book_id: int, user: str = Depends(get_current_user)):
#     if not user:
#         raise HTTPException(status_code=401, detail="Not authenticated")
#     if user.get("fk_rol") != 1:
#         raise HTTPException(status_code=403, detail="Access forbidden: Admins only")

#     return {"message": f"Book with ID {book_id} deleted successfully."}
