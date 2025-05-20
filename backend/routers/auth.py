# backend/routers/auth.py

from fastapi import APIRouter, HTTPException, status, Depends
from ..schemas.auth import UserRegister, UserLogin
from ..dependencies import get_database
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(prefix="/auth", tags=["auth"])

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user: UserRegister,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    # Verifica si el email ya existe
    if await db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    # Crea usuario con contraseña hasheada
    hashed = pwd_context.hash(user.password)
    await db.users.insert_one({"email": user.email, "password": hashed})
    return {"msg": "Usuario creado correctamente"}

@router.post("/login")
async def login(
    credentials: UserLogin,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    user = await db.users.find_one({"email": credentials.email})
    if not user or not pwd_context.verify(credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({"sub": str(user["_id"])})
    return {"access_token": access_token, "token_type": "bearer"}
