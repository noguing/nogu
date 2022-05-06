from datetime import datetime

from bson import ObjectId
from fastapi import FastAPI, Cookie
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse

from models.oauth_client import OauthClient
from models.team import Team
from models.user import User
from objects import request
from objects.glob import get_url

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/oauth/token")
async def user_login(code: str):
    client = request.user_authorize(code)
    if client is OauthClient:
        await client.save()
        await User(id=client.id, username=client.username).save()
        response = RedirectResponse(url=get_url("home"))
        response.set_cookie(key="token", value=client.token)
        return response
    else:
        raise HTTPException(400)


@app.post("/team/create")
async def create_team(name: str, token: str = Cookie(None)):
    user = await OauthClient.authorize_token(token)
    team = Team(leader=user, name=name, creation_time=datetime.now(), users=[ObjectId(user.id)])
    await team.save()
    return team


@app.post("/team/me")
async def get_my_teams(token: str = Cookie(None)):
    user = await OauthClient.authorize_token(token)
    return Team.from_member(ObjectId(user.id))

