from fastapi import APIRouter
from fastapi import Depends
from app.services.auth_service import get_current_user
from app.models.user import User


sales = APIRouter()

@sales.get("/sales/", tags=["sales"])
async def read_sales(user: User = Depends(get_current_user)):
    return {"message": "List of sales"}

@sales.post("/sales/", tags=["sales"])
async def create_sell(user: User = Depends(get_current_user)):
    return {"message": "Sell created"}

@sales.get("/sales/{sales_id}", tags=["sales"])
async def get_sell(sales_id: int, user: User = Depends(get_current_user)):
    return {"message": f"Details of sell {sales_id}"}

@sales.put("/sales/{sales_id}", tags=["sales"])
async def update_sell(sales_id: int, user: User = Depends(get_current_user)):
    return {"message": f"Sell {sales_id} updated"}

@sales.delete("/sales/{sales_id}", tags=["sales"])
async def delete_sell(sales_id: int, user: User = Depends(get_current_user)):
    return {"message": f"Sell {sales_id} deleted"}