from fastapi import FastAPI, Depends
from typing import Annotated, List, Optional
from pydantic import BaseModel

from sqlalchemy.orm import Session

import models
from database import engine, SessionLocal

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Todos(BaseModel):
    id: Optional[int]
    title: str
    description: str
    status: bool


class TodosInDB(Todos):
    id: int
    title: str
    description: str
    status: bool


@app.post("/create-todo")
async def create_todos(todo: Todos, db: Annotated[Session, Depends(get_db)]):
    new_todo = models.Todos(
        title=todo.title, description=todo.description, status=todo.status
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return {"data": new_todo}


@app.get("/all-todos", response_model=List[TodosInDB])
async def get_all_todos(db: Annotated[Session, Depends(get_db)]):
    todos = db.query(models.Todos).all()
    return todos
