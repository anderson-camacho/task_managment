from pydantic import BaseModel, EmailStr, Field

class UserRegister(BaseModel):
    email: EmailStr = Field(
        ...,
        description="Correo electrónico válido del usuario"
    )
    password: str = Field(
        ...,
        min_length=6,
        max_length=128,
        description="Contraseña segura (al menos 6 caracteres)"
    )

class UserLogin(BaseModel):
    email: EmailStr = Field(
        ...,
        description="Correo electrónico registrado"
    )
    password: str = Field(
        ...,
        description="Contraseña del usuario"
    )
