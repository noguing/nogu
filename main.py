from fastapi import FastAPI
from starlette.responses import RedirectResponse

from objects import request, glob
from objects.glob import get_url

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/oauth/token")
async def user_login(code: str):
    authorization = request.user_authorize(code)
    await glob.db_oauth_clients.update_one({"token": authorization['token']}, {"$set": authorization.copy()},
                                           upsert=True)
    response = RedirectResponse(url=get_url("home"))
    response.set_cookie(key="token", value=authorization['token'])
    return response

if __name__ == '__main__':
    print(get_url("test"))