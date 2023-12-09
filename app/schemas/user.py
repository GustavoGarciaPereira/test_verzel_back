from typing import List, Optional
from pydantic import BaseModel, EmailStr

from app.schemas import Car


class UserBase(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None


# Esquema para criar um Usuário (sem ID e sem carros)
class UserCreate(UserBase):
    username: str
    password: str


# Esquema para atualizar um Usuário (todos os campos são opcionais)
class UserUpdate(UserBase):
    name: Optional[str] = None
    email: Optional[str] = None


# Esquema para leitura de User (inclui o ID e lista de carros)
class User(UserBase):
    id: int
    cars: List[Car] = []
    hashed_password: str

    class Config:
        orm_mode = True


# Token schema
