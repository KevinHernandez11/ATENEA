from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base

class Purchase(Base):
    id = Column(Integer, primary_key=True, index=True)
    fk_sale_id = Column(Integer, ForeignKey("sales.id"))
    fk_books_id = Column(Integer, ForeignKey("books.id"))
    quantity = Column(Integer)
    unit_price = Column(Integer)
    total_price = Column(Integer)
    book = relationship("Books", back_populates="sales")

