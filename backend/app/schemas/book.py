from pydantic import BaseModel
from typing import Optional, List

class BookBase(BaseModel):
    name: str
    author: str
    description: str

class BookCreate(BookBase):
    fk_category: Optional[int] = None


class BookResponse(BookBase):
    content: Optional[str] = None

    class Config:
        orm_mode = True

class BookUpdate(BaseModel):
    name: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None

class BookDelete(BaseModel):
    id: int




from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID

# Base común
class BookBase(BaseModel):
    name: str
    author: str
    description: str

# Crear libro
class BookCreate(BookBase):
    fk_category: Optional[str] = None

# Respuesta al obtener un libro
class BookResponse(BookBase):
    name: str
    author: str
    description: str
    content: Optional[str] = None

    class Config:
        orm_mode = True

# Actualizar libro
class BookUpdate(BaseModel):
    name: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    fk_category: Optional[UUID] = None

# Eliminar libro
class BookDelete(BaseModel):
    id: UUID
