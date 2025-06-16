from pydantic import BaseModel
from uuid import UUID 

class PurchaseRequest(BaseModel):
    payment_method_id: str
    amount: float