from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.services.auth_service import get_current_user
from app.schemas.book import BookResponse , BookCreate , BookUpdate , ContentBook
from sqlalchemy.orm import Session
from app.models.book import Books
from app.core.database import get_db 
from app.services.auth_service import get_current_user
from app.models.user import User
from app.services.dependencies import AuthService
from uuid import UUID, uuid4
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import os
import requests

load_dotenv()

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
        fk_user_id= auth_user.id,  # Assuming the book is linked to the user who created it
        state= True if auth_user.rol.name == "Admin" else False,  # Only Admins can set state to True
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



@books.delete("/{book_id}", tags=["books"])
async def delete_book(book_id: UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    auth_user = AuthService.auth_rol_user_books(user)

    if not auth_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    book = db.query(Books).filter(Books.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book.state = "Deleted"  # Assuming you want to mark the book as deleted instead of removing it
    
    db.commit()


    return {"message": "Book deleted successfully"}


cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET"),
    secure=True
)

@books.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not file.filename.endswith(".pdf"):
        return {"error": "Solo se permiten archivos PDF"}

    # Leer el contenido del archivo
    contents = await file.read()

    try:
        # Subir a Cloudinary
        result = cloudinary.uploader.upload(
            contents,
            resource_type="raw",  # Necesario para PDF u otros archivos no imagen
            public_id="uploaded_text_file",  # Replace with a static or dynamic identifier
            folder="pdfs/"  # Opcional: guarda en carpeta específica
        )
        
        new_book = Books(
            content=result["secure_url"],  # Guarda la URL del PDF
            state_content=True  # Asumiendo que quieres marcar el contenido como disponible
        )

        db.add(new_book)
        db.commit()
        db.refresh(new_book)

        return {
            "message": "Archivo subido con éxito",
            "url": result["secure_url"]
        }
    

    except Exception as e:
        return {"error": "Error al subir a Cloudinary", "details": str(e)}


@books.post("/Text")
async def upload_text(Book: ContentBook, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    auth_user = AuthService.auth_rol_user_books(user)
 
    filename = f"{uuid4()}.txt"
    with open(filename, "w", encoding="utf-8") as archivo:
        archivo.write(Book.content)

    try:
        # Subir a Cloudinary
        result = cloudinary.uploader.upload(
            filename,  # Nombre del archivo local
            resource_type="raw",  # Necesario para archivos de texto
            folder="BooksContent/"  # Opcional: guarda en carpeta específica
        )

        os.remove(filename)  # Eliminar el archivo local después de subirlo

        new_book = Books(
            content=result["secure_url"],  # Guarda la URL del archivo de texto
            content_state=True,  # Asumiendo que quieres marcar el contenido como disponible
            fk_user_id=auth_user.id,  # Asociar el contenido del libro al usuario logueado  
        )

        db.add(new_book)
        db.commit()
        db.refresh(new_book)

        return {
            "message": "Archivo de texto subido con éxito",
            "url": result["secure_url"]
        }
    
    except Exception as e:
        return {"error": "Error al subir a Cloudinary", "details": str(e)}
    

@books.get("/books/{book_id}/content", tags=["books"])
async def get_book_content(book_id: UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    auth_user = AuthService.auth_rol_user_books(user)

    if not auth_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    book = db.query(Books).filter(Books.id == book_id).first()

    if not book or not book.content:
        raise HTTPException(status_code=404, detail="Book content not found")
    
    response = requests.get(book.content)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Content not found")
    
    
    return ContentBook(
        content=response.text
    )