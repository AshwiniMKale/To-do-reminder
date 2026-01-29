from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
import models,schemas,crud
from database import SessionLocal,engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="TO-DO-Priority-API")

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/tasks",response_model=schemas.TaskResponse)
def add_task(task:schemas.TaskCreate,db:Session=Depends(get_db)):
    return crud.create_task(db,task)

@app.get("/tasks",response_model=list[schemas.TaskResponse]) 
def lists_task(db:Session=Depends(get_db)):
    return crud.get_task(db)

@app.put("/tasks/{task_id}/complete", response_model=schemas.TaskResponse)
def mark_task_completed(task_id: int, db: Session = Depends(get_db)):
    task = crud.mark_completed(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task