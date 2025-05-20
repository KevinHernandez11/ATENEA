from fastapi import FastAPI
from app.routes.routes import router

app = FastAPI(title="ATENEA", description="API for ATENEA", version="0.1.0")

app.include_router(router)

