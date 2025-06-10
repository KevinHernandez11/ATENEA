from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.models.base import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid 

class Rol(Base):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
    description = Column(String)

    users = relationship("User", back_populates="rol")

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    hashed_password = Column(String)
    fk_rol = Column(UUID(as_uuid=True), ForeignKey("roles.id"))
    state = Column(String, default="active")

    rol = relationship("Rol", back_populates="users")
    profile = relationship("UserProfile", back_populates="user", uselist=False)


class UserProfile(Base):

    __tablename__ = "profile_user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fk_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    fk_books_id = Column(UUID(as_uuid=True), ForeignKey("books.id"), nullable=True)
    books_history = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())


    user = relationship("User", back_populates="profile")
    book = relationship("Books", back_populates="user_profiles")
