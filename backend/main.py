
from fastapi import FastAPI
from core.database import db_dependency, initdb
from core.utils import export_openapi_to_json
from sqlalchemy import text
from models.database_models import *
from api.routers import router
from pathlib import Path

app = FastAPI(title="FastAPI Backend", description="Backend API for the application", version="1.0.0")


@app.on_event("startup")
def on_startup():
    initdb()
    
    output_file = Path("../openapi.json")
    export_openapi_to_json(app, output_file=output_file)


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

@app.get("/openapi", tags=["OpenAPI"])
async def get_openapi():
    openapi_schemas = app.openapi()["components"]["schemas"]
    data = { key: value for key, value in openapi_schemas.items() if key != "HTTPValidationError" and key != "ValidationError" }
    for key, value in data.items():
        # print("VALL", value["properties"])
        if "properties" in value:
            
            properties = value["properties"]
            for prop_key, prop_value in properties.items():
                if "$ref" in prop_value:
                    ref_key = prop_value["$ref"].split("/")[-1]
                    if ref_key in data:
                        properties[prop_key] = data[ref_key]
    return app.openapi()
