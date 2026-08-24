
from fastapi import FastAPI
from core.database import db_dependency, initdb
from sqlalchemy import text
from models.database_models import *
from api.routers import router

app = FastAPI()


@app.on_event("startup")
def on_startup():
    initdb()


@app.get("/")
async def heartbeat():
    return {"message": "Server is running!"}


@app.get("/db")
async def health_check_db(db: db_dependency):
    try:
        db.execute(text("SELECT 1"))
        return { "message": "Database is reachable!"}
    except Exception as e:
        return { "error": f"Error: {str(e)}"}
    
app.include_router(router=router, tags=["API ENDPOINTS"])