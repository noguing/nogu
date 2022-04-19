from typing import Optional

from fastapi import FastAPI
from fastapi.params import Query

from objects import glob

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/beatmap/latest")
async def latest_beatmap(limit: Optional[int] = Query(10, le=50), offset: int = 0):
    cursor = glob.db_beatmap.find().sort("last_updated", -1).limit(limit).skip(offset)
    return await cursor.to_list(length=100)
