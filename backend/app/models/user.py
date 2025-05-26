from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime
import uuid 

Base = declarative_base()

class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True, nullable=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)

    users = relationship("User", back_populates="rol")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    hashed_password = Column(String)
    fk_rol = Column(Integer, ForeignKey("roles.id"))
    rol = relationship("Rol", back_populates="users")

