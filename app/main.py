# FastAPI je moderní webový framework pro Python, který umožňuje snadno vytvářet API.
from fastapi import FastAPI
# Pydantic je knihovna pro validaci dat a serializaci
from pydantic import BaseModel
from . import models, database

app = FastAPI(title="Task Tracker")
models.Base.metadata.create_all(bind=database.engine)

# definice endpointu
@app.get("/")

def read_root():
    return {"message": "Task tracker bezi..."}


@app.post("/tasks", response_model=schemas.Task)
def create_tasks(task:schemas.TaskCreate, db:Session=Depends(get_db)):
    db_task=models.Task(title=task.title,description=task.description)
    db.add(db_task)
    db.commit()
    db.refresh(db.task)
    return db_task

@app.get("/tasks", response_model=list[schemas.Task])

def list_tasks(db:Session = Depends(get_db)):
    # vracení seznamu všech tasků
    return db.query(models.Task).all()
    
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()