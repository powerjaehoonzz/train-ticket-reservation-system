from fastapi import FastAPI

from router.station import router as station_router
from router.train import router as train_router

app = FastAPI()

app.include_router(station_router)
app.include_router(train_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
