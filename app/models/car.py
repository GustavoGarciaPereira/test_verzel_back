from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from .base import Base

# Modelo Car


class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    marca = Column(String, index=True)
    modelo = Column(String, index=True)
    price = Column(Float)
    url_imagem = Column(String)
    user_id = Column(
        Integer, ForeignKey("users.id")
    )  # Chave estrangeira para associar o carro ao usuário

    # Relação com o modelo User
    user = relationship("User", back_populates="cars")
