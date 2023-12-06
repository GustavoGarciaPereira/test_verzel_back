from typing import Optional
from pydantic import BaseModel


# Esquema Base para Car
class CarBase(BaseModel):
    nome: str
    marca: str
    modelo: str
    price: float
    url_imagem: str


# Esquema para criar um Carro (sem ID, que é gerado automaticamente)
class CarCreate(CarBase):
    pass


# Esquema para atualizar um Carro (todos os campos são opcionais)
class CarUpdate(CarBase):
    nome: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    price: Optional[float] = None
    url_imagem: Optional[str] = None

# Esquema para leitura (inclui o ID)


class Car(CarBase):
    id: int

    class Config:
        orm_mode = True


# Esquema Base para User
class UserBase(BaseModel):
    name: str
    email: str


# Esquema para criar um Usuário (sem ID)
class UserCreate(UserBase):
    car_id: int


# Esquema para atualizar um Usuário (todos os campos são opcionais)
class UserUpdate(UserBase):
    name: Optional[str] = None
    email: Optional[str] = None
    car_id: Optional[int] = None


# Esquema para leitura (inclui o ID)
class User(UserBase):
    id: int
    car_id: int

    class Config:
        orm_mode = True
