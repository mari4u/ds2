from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List,Optional
from sqlalchemy import create_engine,Column,Integer,String,DateTime
from sqlalchemy.orm import sessionmaker,declarative_base
from datetime import datetime
from pydantic import validator

eng=create_engine("sqlite:///./tasks.db",connect_args={"check_same_thread":False})
ses=sessionmaker(bind=eng)
base=declarative_base()
class TaskDB(base):
  __tablename__="tasks"
  id=Column(Integer,primary_key=True,index=True)
  title=Column(String)
  description=Column(String)
  status=Column(String)
  priority=Column(Integer)
  created=Column(DateTime)
app=FastAPI()
@app.on_event("startup")
def startup():
    base.metadata.create_all(bind=eng)
class Task(BaseModel):
  title:str
  description:str
  status:str
  priority:int
  @validator("status")
  def check(cls,v):
    a=["pending","in work","completed"]
    if v not in a:
      raise ValueError("status: pending/in work/completed")
    return v

@app.post("/tasks/")
def create(task:Task):
  db=ses()
  ntask=TaskDB(title=task.title,description=task.description,status=task.status,priority=task.priority,created=datetime.now())
  db.add(ntask)
  db.commit()
  return {"message":"task made"}

@app.get("/tasks/")
def get():
  db=ses()
  t=db.query(TaskDB).all()
  return t

@app.put("/tasks/{task_id}")
def put(task_id:int,task:Task):
  db=ses()
  dbt=db.query(TaskDB).filter(TaskDB.id==task_id).first()
  if not dbt:
    raise HTTPException(status_code=404,detail="not find")
  dbt.title=task.title
  dbt.description=task.description
  dbt.status=task.status
  dbt.priority=task.priority
  db.commit()
  return {"message":"task update"}

@app.delete("/tasks/{task_id}")
def delete(task_id:int):
  db=ses()
  dbt=db.query(TaskDB).filter(TaskDB.id==task_id).first()
  if not dbt:
    raise HTTPException(status_code=404,detail="not find")
  db.delete(dbt)
  db.commit()
  return {"message":"task deleted"}

@app.get("/tasks/sort/")
def sort(by:str):
  db=ses()
  if by=="title":
    t=db.query(TaskDB).order_by(TaskDB.title).all()
  elif by=="status":
    t=db.query(TaskDB).order_by(TaskDB.status).all()
  elif by=="date":
    t=db.query(TaskDB).order_by(TaskDB.created).all()
  else:
    raise HTTPException(status_code=400,detail="wrong parameter")
  return t

@app.get("/tasks/top/")
def top(n:int):
  db=ses()
  t=db.query(TaskDB).order_by(TaskDB.priority.desc()).limit(n).all()
  return t

@app.get("/tasks/search/")
def search(query:str):
  db=ses()
  t=db.query(TaskDB).all()
  res=[]
  for i in t:
    if query.lower() in i.title.lower() or query.lower() in i.description.lower():
      res.append(i)
  return res