from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

Base = declarative_base()

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    marca = Column(String, index=True)
    modelo = Column(String, index=True)
    price = Column(Float)
    url_imagem = Column(String)


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


@app.get("/populate-db")
def populate_db(db: Session = Depends(get_db)):
    for car_data in carros_data:
        car = Car(**car_data)
        db.add(car)
    db.commit()
    return {"message": "Database populated with car data"}


@app.get("/cars")
def list_cars(db: Session = Depends(get_db)):
    return db.query(Car).all()
