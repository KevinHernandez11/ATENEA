from sqlalchemy import Column, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime
from app.models import Base  # Asegúrate de tener esto en tu proyecto

class Purchase(Base):
    __tablename__ = "purchase_data"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"))  # Relación con libro

    stripe_payment_id = Column(String, unique=True, nullable=False)  # ej: pi_1N...
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="COP")
    status = Column(String(30), nullable=False)
    method = Column(String(50), default="card")

    card_last4 = Column(String(4))
    card_brand = Column(String(20))

    refunded = Column(Boolean, default=False)
    extra_metadata = Column(JSONB, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="purchases")
    book_purchase = relationship("Books", back_populates="purchases")


