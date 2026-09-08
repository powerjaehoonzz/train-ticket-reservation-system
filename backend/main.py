from fastapi import FastAPI

from router.station import router as station_router
from router.train import router as train_router
from router.train_schedule import router as train_schedule_router
from router.reservation import router as reservation_router
from router.auth import router as auth_router

app = FastAPI()

app.include_router(station_router)
app.include_router(train_router)
app.include_router(train_schedule_router)
app.include_router(reservation_router)
app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
