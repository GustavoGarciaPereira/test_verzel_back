from typing import List, Optional
from pydantic import BaseModel, EmailStr


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
