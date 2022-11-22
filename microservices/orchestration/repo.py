from sqlalchemy.orm import Session
from common.schemas import saga
from . import models


def retrieve_sagas(db: Session, saga_id: str):
    return db.query(models.Saga).filter(models.Saga.uuid == saga_id).all()


def retrieve_all_sagas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Saga).offset(skip).limit(limit).all()


def create_saga(db: Session, saga_data: saga.SagaCreate):
    db_item = models.Saga(**saga_data.dict())
    db.add(db_item)
    db.commit()
