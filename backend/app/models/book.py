from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base
import uuid

class Categories(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)

    books = relationship("Books", back_populates="category")

class Books(Base):
    __tablename__ = "books"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
    author = Column(String)
    description = Column(String)
    fk_categories = Column(UUID(as_uuid=True), ForeignKey("categories.id"))
    fk_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    content = Column(String)
    state = Column(Boolean, default=False)
    book_state = Column(String, default="new")
    content_state = Column(Boolean)

    category = relationship("Categories", back_populates="books")
    stock = relationship("Stock", back_populates="book_stock")
    chapters = relationship("book_chapters", back_populates="book_cap", cascade="all, delete-orphan")
    user = relationship("User", back_populates="books")

class Stock(Base):
    __tablename__ = "stock"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fk_book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"))
    quantity = Column(Integer)
    last_update = Column(DateTime)

    book_stock = relationship("Books", back_populates="stock")


class book_chapters(Base):
    __tablename__ = "book_chapters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fk_book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"))
    chapter_number = Column(Integer)
    title = Column(String)
    content = Column(String)

    book_cap = relationship("Books", back_populates="chapters")
