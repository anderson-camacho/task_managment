from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
import os

# 1. Define el esquema OAuth2 para extraer el token del header Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Inyecta la base de datos configurada en main.py
def get_database(request: Request) -> AsyncIOMotorDatabase:
    return request.app.mongodb

# 2. Función para obtener la base de datos desde la aplicación
def get_database() -> AsyncIOMotorDatabase:
    from fastapi import Request
    # Requiere que en main.py asignes app.mongodb = client.get_default_database()
    from fastapi import Depends
    from fastapi import FastAPI
    app = FastAPI.instance  # placeholder, en realidad usarás Request.app.mongodb
    return app.mongodb

# 3. Dependencia para obtener el usuario actual
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncIOMotorDatabase = Depends(get_database)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autorizado o token inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            os.getenv("SECRET_KEY"),
            algorithms=[os.getenv("ALGORITHM")]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise credentials_exception

    # Puedes devolver sólo los campos que necesites
    return {"id": str(user["_id"]), "email": user["email"]}