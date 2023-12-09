from sqlalchemy.orm import Session
from app import models, schemas


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
