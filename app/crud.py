from . import models
from . import schemas

from sqlalchemy.orm import Session


def get_car(db: Session, car_id: int):
    return db.query(models.Car).filter(models.Car.id == car_id).first()


def get_cars(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Car).offset(skip).limit(limit).all()


def create_car(db: Session, car: schemas.CarCreate):
    # Verificar se o usuário existe
    user = db.query(models.User).filter(models.User.id == car.user_id).first()
    if not user:
        raise ValueError("User ID not found")

    db_car = models.Car(**car.dict())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


def update_car(db: Session, car_id: int, car: schemas.CarUpdate):
    db_car = get_car(db, car_id)
    if db_car:
        update_data = car.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_car, key, value)
        db.commit()
        db.refresh(db_car)
    return db_car


def delete_car(db: Session, car_id: int):
    db_car = get_car(db, car_id)
    if db_car:
        db.delete(db_car)
        db.commit()
    return db_car



from passlib.context import CryptContext

# Contexto para lidar com hashes de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

#================================================================
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    
    print(user)
    db_user = models.User(
        username=user.username, hashed_password=hashed_password, name=user.name, email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print(f'\n\n\n{hashed_password}\n\n\n')
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        update_data = user.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
