from fastapi import APIRouter , Depends, HTTPException
from app.services.auth_service import get_current_user
from app.schemas.book import BookResponse , BookCreate , BookUpdate
from sqlalchemy.orm import Session
from app.models.book import Books
from app.core.database import get_db 
from app.services.auth_service import get_current_user
from app.models.user import User
from app.services.dependencies import AuthService
from uuid import UUID

books = APIRouter()

# This is a sample route for listing books
@books.get("/books/", tags=["books"])
async def read_books(user: User = Depends(get_current_user)):
    auth_user = AuthService.auth_rol_user_books(user)
    if not auth_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    return {"message": "List of books", "user": auth_user.email}

#Esta ruta es pra crear un libro
@books.post("/books/", tags=["books"], response_model=BookResponse)
async def create_book(book: BookCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    auth_user = AuthService.auth_rol_user_books(user)

    if not auth_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    new_book = Books(
        name=book.name,
        author=book.author,
        description=book.description,
        state=(auth_user.rol.name == "Admin")
        
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    
    return BookResponse(
        name=book.name,
        author=book.author,
        description=book.description
    )


#Esta ruta es para obtener un libro por su ID
@books.get("/{book_id}")
async def get_book(book_id: UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    auth_user = AuthService.auth_rol_user_books(user)
    print(auth_user)
    if not auth_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    book = db.query(Books).filter(Books.id == book_id).first()
    print(book)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return BookResponse(
        name=book.name,
        author=book.author,
        description=book.description,
        content=book.content.content if book.content.content else None
    )
    
# Esta ruta es para actualizar un libro por su ID
@books.put("/{book_id}", tags=["books"], response_model=BookResponse)
async def update_book(book_id: UUID, book: BookUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    auth_user = AuthService.auth_rol_user_books(user)

    if not auth_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    existing_book = db.query(Books).filter(Books.id == book_id).first()

    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.name:
        existing_book.name = book.name
    if book.author:
        existing_book.author = book.author
    if book.description:
        existing_book.description = book.description
    if book.fk_category:
        existing_book.fk_category = book.fk_category

    db.commit()
    db.refresh(existing_book)

    return BookResponse(
        name=existing_book.name,
        author=existing_book.author,
        description=existing_book.description,
        content=existing_book.content.content if existing_book.content.content else None
    )



# @books.delete("/{book_id}", tags=["books"])
# async def delete_book(book_id: int, user: str = Depends(get_current_user)):
#     if not user:
#         raise HTTPException(status_code=401, detail="Not authenticated")
#     if user.get("fk_rol") != 1:
#         raise HTTPException(status_code=403, detail="Access forbidden: Admins only")

#     return {"message": f"Book with ID {book_id} deleted successfully."}
