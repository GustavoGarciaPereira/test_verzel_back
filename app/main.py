from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from typing import List

from . import crud
from . import schemas

Base = declarative_base()


# class Car(Base):
#     __tablename__ = "cars"

#     id = Column(Integer, primary_key=True, index=True)
#     nome = Column(String, index=True)
#     marca = Column(String, index=True)
#     modelo = Column(String, index=True)
#     price = Column(Float)
#     url_imagem = Column(String)


app = FastAPI()


SQLALCHEMY_DATABASE_URL = "postgresql://user:password@db:5432/mydatabase"
# Altere a URL acima para a configuração do seu banco de dados

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Inicialize o Base com o engine para criar as tabelas no DB
Base.metadata.create_all(bind=engine)

carros_data = [
    {
        "nome": "Fusca",
        "marca": "Volkswagen",
        "modelo": "Fusca",
        "price": 10000,
        "url_imagem": "https://upload.wikimedia.org/wikipedia/commons/4/45/VW_K%C3%A4fer%2C_Bj._1958_%282015-09-12_3727_b2%29.JPG"
    },
    {
        "nome": "Fusca",
        "marca": "Volkswagen",
        "modelo": "Fusca",
        "price": 10001,
        "url_imagem": "https://upload.wikimedia.org/wikipedia/commons/4/45/VW_K%C3%A4fer%2C_Bj._1958_%282015-09-12_3727_b2%29.JPG"
    },
    {
        "nome": "Fusca",
        "marca": "Volkswagen",
        "modelo": "Fusca",
        "price": 10002,
        "url_imagem": "https://upload.wikimedia.org/wikipedia/commons/4/45/VW_K%C3%A4fer%2C_Bj._1958_%282015-09-12_3727_b2%29.JPG"
    }
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Dependência para injetar a sessão do SQLAlchemy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.get("/populate-db")
# def populate_db(db: Session = Depends(get_db)):
#     for car_data in carros_data:
#         car = Car(**car_data)
#         db.add(car)
#     db.commit()
#     return {"message": "Database populated with car data"}


@app.post("/cars/", response_model=schemas.Car)
def create_car(car: schemas.CarCreate, db: Session = Depends(get_db)):
    return crud.create_car(db=db, car=car)


@app.get("/cars/", response_model=List[schemas.Car])
def read_cars(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cars = crud.get_cars(db, skip=skip, limit=limit)
    return cars


@app.get("/cars/{car_id}", response_model=schemas.Car)
def read_car(car_id: int, db: Session = Depends(get_db)):
    db_car = crud.get_car(db, car_id=car_id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car


@app.put("/cars/{car_id}", response_model=schemas.Car)
def update_car(car_id: int, car: schemas.CarUpdate, db: Session = Depends(get_db)):
    db_car = crud.update_car(db, car_id, car)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car


@app.delete("/cars/{car_id}", response_model=schemas.Car)
def delete_car(car_id: int, db: Session = Depends(get_db)):
    db_car = crud.delete_car(db, car_id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car
#=================================================================================================


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user



