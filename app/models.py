from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
# from database import Base


class Car(Base):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    marca = Column(String, index=True)
    modelo = Column(String, index=True)
    price = Column(Float)
    url_imagem = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))  # Chave estrangeira para associar o carro ao usuário

    # Relação com o modelo User
    user = relationship("User", back_populates="cars")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    username = Column(String,unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    # Relação com o modelo Car
    cars = relationship("Car", order_by=Car.id, back_populates="user")