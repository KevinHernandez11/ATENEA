from jose import JWTError, jwt
from dotenv import load_dotenv
from app.core.database import SessionLocal
from sqlalchemy.orm import Session
from app.models.user import User
import os
import datetime

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGHORITHM = os.getenv("ALGHORITHM")

def create_token(user_id: str):
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        payload = {
            "id":str(user.id),
            "role": user.fk_rol,
             'exp':datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
        }

        token = jwt.encode(payload, SECRET_KEY, ALGHORITHM)
        return token
    finally:
        db.close()

#manejar estados
#UUID
#Cambiar el token para que sea un UUID

