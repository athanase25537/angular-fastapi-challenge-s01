from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated
from fastapi import Depends 
from dotenv import load_dotenv
from sqlmodel import SQLModel


load_dotenv()

DATABASE_URL = getenv("DATABASE_URL", "")
print(DATABASE_URL)

engine = create_engine(url=DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

def initdb():
    print("ok")
    SQLModel.metadata.create_all(bind=engine)   
    
    
def get_db():
    
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]