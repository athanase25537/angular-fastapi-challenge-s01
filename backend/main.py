
from fastapi import FastAPI
from core.database import db_dependency, initdb
from sqlalchemy import text
from models.database_models import *
from api.routers import router

app = FastAPI(title="FastAPI Backend", description="Backend API for the application", version="1.0.0")


@app.on_event("startup")
def on_startup():
    initdb()


@app.get("/", tags=["Heartbeat"])
async def heartbeat():
    return {"message": "Server is running!"}


@app.get("/db", tags=["Heartbeat"])
async def health_check_db(db: db_dependency):
    try:
        db.execute(text("SELECT 1"))
        return { "message": "Database is reachable!"}
    except Exception as e:
        return { "error": f"Error: {str(e)}"}
    
app.include_router(router=router)