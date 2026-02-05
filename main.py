from fastapi import FastAPI,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models,schemas,crud
from database import SessionLocal,engine
from auth import get_db,create_access_token,get_current_user

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="TO-DO-Priority-API")

# def get_db():
#     db=SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

#signup
@app.post("/signup",response_model=schemas.UserOut)
def signup(user:schemas.UserCreate,db:Session=Depends(get_db)):
    db_user = crud.get_user_by_email(db,user.email)
    if db_user:
        raise HTTPException(status_code=400,detail="Email already exists")
    created = crud.create_user(db,user)
    return created

#login
@app.post("/token",response_model=schemas.Token)
def login_using_access_token(form_data:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    user = crud.authenticate_user(db,form_data.username,form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect emailid or passwoed")
    access_token = create_access_token(data={"sub":user.email})
    return  {"access_token":access_token,"token_type":"bearer"}

#current user
@app.get("/users/me",response_model=schemas.UserOut)
def read_user_me(current_user:models.User=Depends(get_current_user)):
    return current_user

@app.get("/")
def root(user=Depends(get_current_user)):
    return {"msg": "hello"}

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

