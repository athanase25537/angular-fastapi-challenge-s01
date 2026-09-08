from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated
from fastapi import Depends 
from dotenv import load_dotenv
from sqlmodel import SQLModel, Session


load_dotenv()

DATABASE_URL = getenv("DATABASE_URL", "sqlite:///./app.db")

# SQLite is useful for a zero-configuration local start.  PostgreSQL settings in
# DATABASE_URL continue to work unchanged.
engine_options = {"connect_args": {"check_same_thread": False}} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(url=DATABASE_URL, **engine_options)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine, class_=Session)

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
