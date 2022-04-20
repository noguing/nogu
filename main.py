from fastapi import FastAPI

from objects import request, glob

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/oauth/token")
def user_login(code: str):
    authorization = request.user_authorize(code)
    await glob.db_oauth_clients.update_one({"token": authorization['token']}, {"$set": authorization.copy()}, upsert=True)
    return authorization
