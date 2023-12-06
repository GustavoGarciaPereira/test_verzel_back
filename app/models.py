from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
# from database import Base


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    marca = Column(String, index=True)
    modelo = Column(String, index=True)
    price = Column(Float)
    url_imagem = Column(String)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    car_id = Column(Integer, ForeignKey('cars.id'))

    car = relationship("Car")
