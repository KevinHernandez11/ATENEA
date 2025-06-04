from pydantic import BaseModel
from typing import Optional, List

class BookBase(BaseModel):
    name: str
    author: str
    description: str

class BookCreate(BookBase):
    fk_category: Optional[int] = None


class BookResponse(BookBase):
    pass

    class Config:
        orm_mode = True

class BookUpdate(BaseModel):
    name: Optional[str] = None
    author: Optional[str] = None
    fk_category: Optional[int] = None

class BookDelete(BaseModel):
    id: int
