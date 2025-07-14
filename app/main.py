from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routes import tasks, allocate
from app.core.db import create_db_and_tables


app = FastAPI(title= "Borrowed Beans Task API")


app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(allocate.router, prefix="/allocate", tags = ["Allocation"])

# Serve static frontend folder
app.mount("/", StaticFiles(directory="app/frontend", html=True), name="frontend")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
