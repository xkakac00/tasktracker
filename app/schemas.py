# Slouzi k validaci vstupu a vystupu API
# pydantic bude kontrolovat typy (str,int, None) a vracet chybu kdyz bude neco spatne
from pydantic import BaseModel, ConfigDict

class TaskBase(BaseModel):
    title:str 
    description: str | None = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id:int
    model_config = ConfigDict(from_attributes=True)



      