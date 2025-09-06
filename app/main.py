# FastAPI je moderní webový framework pro Python, který umožňuje snadno vytvářet API.
from fastapi import FastAPI,Depends, HTTPException
from sqlalchemy.orm import Session
# Pydantic je knihovna pro validaci dat a serializaci
from pydantic import BaseModel
from . import models, database, schemas

app = FastAPI(title="Task Tracker")
models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# definice endpointu
@app.get("/")

def read_root():
    return {"message": "Task tracker bezi..."}


@app.post("/tasks", response_model=schemas.Task)
def create_tasks(task:schemas.TaskCreate, db:Session=Depends(get_db)):
    db_task=models.Task(title=task.title,description=task.description)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks", response_model=list[schemas.Task])

def list_tasks(db:Session = Depends(get_db)):
    # vracení seznamu všech tasků
    return db.query(models.Task).all()


@app.get("/tasks/{task_id}",response_model=schemas.Task)

def get_task(task_id, db:Session= Depends(get_db)):
    obj = db.get(models.Task, task_id)
    if obj is None:
        raise HTTPException(status_code=404,detail="Task not found")
    return obj

# Kdybych nechal status kod jako 204 - server by mi nevratil zadny obsah 
@app.delete("/tasks/{task_id}", status_code=200)

def delete_task(task_id:int, db:Session=Depends(get_db)):
    obj = db.get(models.Task, task_id)
    if obj is None:
        raise HTTPException(status_code=404,detail="Task not found")
    db.delete(obj)
    db.commit()
    return {"detail":f"Task {task_id} deleted"}

@app.patch("/tasks/{task_id}", response_model=schemas.Task)

def update_task(task_id:int, payload:schemas.TaskUpdate, db:Session=Depends(get_db)):
    obj = db.get(models.Task, task_id)

    if obj is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if payload.title is not None:
        obj.title = payload.title
    if payload.description is not None:
        obj.description = payload.description
    
    db.commit()
    db.refresh(obj) # natahne aktualni stav
    return obj
    