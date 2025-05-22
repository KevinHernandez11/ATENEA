from pydantic import BaseModel
from typing import Optional, List

class BookBase(BaseModel):
    name: str
    author: str
    description: str

class BookCreate(BookBase):
    pass 

class BookResponse(BookBase):
    id: int
    fk_category: Optional[int] = None

    class Config:
        orm_mode = True

class BookUpdate(BaseModel):
    name: Optional[str] = None
    author: Optional[str] = None
    fk_category: Optional[int] = None

class BookDelete(BaseModel):
    id: int
