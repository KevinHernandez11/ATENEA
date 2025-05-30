from pydantic import BaseModel, Field
from typing import Optional


class Token(BaseModel):
    acces_token : str
    token_type: str = Field(default="bearer")