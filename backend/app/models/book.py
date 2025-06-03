from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    books = relationship("Books", back_populates="category")

#Eliminar las tablas y actualizarlas, gracias
class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    author = Column(String)
    description = Column(String)
    fk_category = Column(Integer, ForeignKey("categories.id"))
    state = Column(String, default="available")
    book_state = Column(String, default="new")  
    category = relationship("Categories", back_populates="books")
    stock = relationship("Stock", back_populates="book")


class Stock(Base):
    __tablename__ = "stock"

    id = Column(Integer, primary_key=True, index=True)
    fk_book_id = Column(Integer, ForeignKey("books.id"))
    quantity = Column(Integer)
    last_update = Column(DateTime)
    book = relationship("Books", back_populates="stock")
