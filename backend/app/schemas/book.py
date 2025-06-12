from pydantic import BaseModel
from typing import Optional
from uuid import UUID  

class BookBase(BaseModel):
    name: str
    author: str
    description: str

class BookCreate(BookBase):
    category: Optional[int] = None


class BookResponse(BookBase):
    content: Optional[str] = None

    class Config:
        orm_mode = True


class BookUpdate(BaseModel):
    name: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    category: Optional[UUID] = None


class BookDelete(BaseModel):
    id: UUID



# class BookListResponse(BaseModel):
#     books: List[BookResponse]

#     class Config:
#         orm_mode = True
#         use_enum_values = True
#         arbitrary_types_allowed = True
#         json_encoders = {
#             UUID: str,
#         }


# class BookCategoryResponse(BaseModel):
#     id: UUID
#     name: str

#     class Config:
#         orm_mode = True
#         use_enum_values = True
#         arbitrary_types_allowed = True
#         json_encoders = {
#             UUID: str,
#         }