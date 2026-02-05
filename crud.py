from sqlalchemy.orm import Session
from models import Task,User
from schemas import TaskCreate,UserCreate
from passlib.context import CryptContext
from typing import List,Optional


pwd_context = CryptContext(schemes=["sha256_crypt"],deprecated = "auto")

#Users
def get_user_by_email(db:Session,email:str) ->Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create_user(db:Session,user:UserCreate)->User:
    hashed_password = pwd_context.hash(user.hashed_password)
    db_user = User(email=user.email,hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password: str,hashed_password:str)->bool:
    return pwd_context.verify(plain_password,hashed_password)

def authenticate_user(db:Session,email:str,password:str)->Optional[User]:
    user = get_user_by_email(db,email)
    if not user:
        return  None
    if not verify_password(password,user.hashed_password):
        return None
    return user

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

