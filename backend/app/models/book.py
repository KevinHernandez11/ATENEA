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


class Book_Content(Base):
    __tablename__ = "book_content"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(String, nullable=True)
    description = Column(String, nullable=True)
    state = Column(String, default="") 

    book = relationship("Books", back_populates="content", uselist=False)


class Books(Base):
    __tablename__ = "books"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
    author = Column(String)
    description = Column(String)
    fk_categories = Column(UUID(as_uuid=True), ForeignKey("categories.id"))
    fk_content = Column(UUID(as_uuid=True), ForeignKey("book_content.id"))
    state = Column(Boolean, default=False)
    book_state = Column(String, default="new")

    category = relationship("Categories", back_populates="books")
    content = relationship("Book_Content", back_populates="book", uselist=False)
    stock = relationship("Stock", back_populates="book_stock")
    chapters = relationship("book_chapters", back_populates="book_cap", cascade="all, delete-orphan")
    user_profiles = relationship("UserProfile", back_populates="book")

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
