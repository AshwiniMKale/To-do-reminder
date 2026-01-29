from sqlalchemy.orm import Session
from models import Task
from schemas import TaskCreate

def create_task(db:Session,task:TaskCreate):
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task(db:Session):
    return db.query(Task).order_by(Task.priority).all()

def mark_completed(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.completed = True
        db.commit()
        db.refresh(task)
    return task    