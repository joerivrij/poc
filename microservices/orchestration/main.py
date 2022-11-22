import asyncio

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import repo, orchestrator, models
from .database import SessionLocal, engine
from common.schemas import saga
from threading import Thread
from common.schemas import sql as schemas
from uuid import uuid4

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    return db


@app.post("/sagas")
async def create_new_flow(tree: schemas.CombinedTree, db: Session = Depends(get_db)):
    uuid = str(uuid4())
    asyncio.create_task(orchestrator.create_saga(uuid=uuid, tree=tree, db=db))

    return {"sagaId": uuid}


@app.get("/sagas/{uuid}")
async def create_new_flow(uuid: str, db: Session = Depends(get_db)):
    return repo.retrieve_sagas(db, uuid)


@app.get("/sagas")
async def create_new_flow(db: Session = Depends(get_db)):
    return repo.retrieve_all_sagas(db)
