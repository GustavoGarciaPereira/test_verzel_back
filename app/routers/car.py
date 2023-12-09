from fastapi import APIRouter, Depends, HTTPException, status
from app import schemas
from app import crud
from app.dependencies import get_db
from app.models import User

# Rotas relacionadas a Car
router = APIRouter()


# @router.get("/populate-db")
# def populate_db(db: Session = Depends(get_db)):
#     for car_data in carros_data:
#         car = Car(**car_data)
#         db.add(car)
#     db.commit()
#     return {"message": "Database populated with car data"}


from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import List, Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Configurações do JWT (substitua com suas próprias chaves)
SECRET_KEY = "12b47320393cafd269a011a4c1cf29949b865e859512fbb0461db71e31b67399"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "user_id": user.id}


@router.get("/usersAlt/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user


# ===================================================================
@router.post("/cars/", response_model=schemas.Car)
def create_car(car: schemas.CarCreate, db: Session = Depends(get_db)):
    try:
        return create_car(db=db, car=car)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# @router.get("/cars/", response_model=List[schemas.Car])
# def read_cars(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
#     # A linha acima garante que o usuário esteja autenticado
#     # Você pode usar 'current_user' para acessar os dados do usuário atual, se necessário


#     cars = crud.get_cars(db, skip=skip, limit=limit)
#     return cars
@router.get("/cars/", response_model=List[schemas.Car])
def read_cars(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # A linha acima garante que o usuário esteja autenticado
    # Você pode usar 'current_user' para acessar os dados do usuário atual, se necessário

    cars = crud.get_cars(db, skip=skip, limit=limit)
    return cars


@router.get("/cars/{car_id}", response_model=schemas.Car)
def read_car(car_id: int, db: Session = Depends(get_db)):
    db_car = crud.get_car(db, car_id=car_id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car


@router.put("/cars/{car_id}", response_model=schemas.Car)
def update_car(car_id: int, car: schemas.CarUpdate, db: Session = Depends(get_db)):
    db_car = crud.update_car(db, car_id, car)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car


@router.delete("/cars/{car_id}", response_model=schemas.Car)
def delete_car(car_id: int, db: Session = Depends(get_db)):
    db_car = crud.delete_car(db, car_id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car


# =================================================================================================
