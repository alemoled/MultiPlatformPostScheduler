from fastapi import FastAPI
from app.routes import router as main_router
from app.scheduler import start_scheduler
from app.database import Base, engine
from app import models


app = FastAPI()
app.include_router(main_router)

@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)
    start_scheduler()
