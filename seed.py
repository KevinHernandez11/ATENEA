# # seed.py
# from sqlalchemy.exc import SQLAlchemyError
# from app.core.database import engine, SessionLocal, Base
# from app.models.user import User

# def seed():
#     # 1. Crea las tablas si no existen
#     Base.metadata.create_all(bind=engine)
    
#     # 2. Crea una sesión
#     session = SessionLocal()
#     try:
#         # 3. Instancia datos de prueba
#         user1 = User(name="Alice Example", email="alice@example.com", phone="1234567890", hashed_password="hashedpassword")

#         # 4. Agrega al session y confirma
#         session.add_all([user1])
#         session.commit()
#         print("✅ Datos seed insertados correctamente")
        
#         # 5. Consulta para verificar
#         users = session.query(User).all()
#         for u in users:
#             print(f"- {u.id}: {u.name} ({u.email})")
#     except SQLAlchemyError as e:
#         session.rollback()
#         print("❌ Error al insertar datos:", e)
#     finally:
#         session.close()

# if __name__ == "__main__":
#     seed()
