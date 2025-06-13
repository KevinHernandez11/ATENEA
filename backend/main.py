from fastapi import FastAPI
from app.routes.register import register
from app.routes.home import home
from app.routes.login import login
from app.routes.books import books
from app.routes.sales import purchase


app = FastAPI(title="ATENEA", description="API for ATENEA", version="0.1.0")

app.include_router(home, prefix="/api/v1", tags=["home"])
app.include_router(register, prefix="/api/v1", tags=["register"])
app.include_router(login, prefix="/api/v1", tags=["login"])
app.include_router(books, prefix="/api/v1", tags=["books"])
app.include_router(purchase, prefix="/api/v1", tags=["sales"])

