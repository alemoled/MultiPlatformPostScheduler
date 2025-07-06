from fastapi import FastAPI
from app.routes import router as main_router
from app.scheduler import start_scheduler

app = FastAPI()
app.include_router(main_router)

@app.on_event("startup")
async def startup():
    start_scheduler()
