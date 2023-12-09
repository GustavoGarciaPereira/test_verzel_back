from fastapi import FastAPI
from app.routers import car, user
from .dependencies import engine
from .models.base import Base

app = FastAPI()

# Inicializa o Base com o engine para criar as tabelas no DB
Base.metadata.create_all(bind=engine)

# Adiciona rotas ao aplicativo
app.include_router(car.router)
app.include_router(user.router)
