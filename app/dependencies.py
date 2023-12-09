from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi.security import OAuth2PasswordBearer
from .config import settings

# Criação do motor de conexão do SQLAlchemy
engine = create_engine(settings.database_url)

# Criação da sessão local do SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos do SQLAlchemy
Base = declarative_base()

# Dependência para obter o token OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Dependência da sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Aqui você pode adicionar funções adicionais de autenticação e segurança
