from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import car, user
from .dependencies import engine
from .models.base import Base

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Inicializa o Base com o engine para criar as tabelas no DB
Base.metadata.create_all(bind=engine)

# Adiciona rotas ao aplicativo
app.include_router(car.router)
app.include_router(user.router)
