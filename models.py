from sqlalchemy import Column,Integer,Boolean,String,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime



class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)    
    email = Column(String,unique=True,index=True,nullable=False)
    hashed_password = Column(String,nullable=False)
    is_active = Column(Boolean,default=True)
    created_at = Column(DateTime,default = datetime.utcnow)

    task = relationship("Task",back_populates="owner")

class Task(Base):
    __tablename__="tasks"
    
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,index=True)
    description = Column(String)
    priority = Column(String)
    completed = Column(Boolean,default=False)
    owner_id  = Column(Integer,ForeignKey("users.id"))
    owner = relationship("User", back_populates="task")
