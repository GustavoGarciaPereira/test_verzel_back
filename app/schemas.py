from typing import List, Optional
from pydantic import BaseModel, EmailStr

# Esquema Base para Car
class CarBase(BaseModel):
    nome: str
    marca: str
    modelo: str
    price: float
    url_imagem: str

# Esquema para criar um Carro (inclui user_id)
class CarCreate(CarBase):
    user_id: int

# Esquema para atualizar um Carro (todos os campos são opcionais)
class CarUpdate(CarBase):
    nome: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    price: Optional[float] = None
    url_imagem: Optional[str] = None

# Esquema para leitura de Carro (inclui o ID)
class Car(CarBase):
    id: int

    class Config:
        orm_mode = True

# Esquema Base para User

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
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    password: str