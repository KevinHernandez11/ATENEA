from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.book import Books

def create_book(title: str, author: str, description: str):
    db: Session = SessionLocal()

    
