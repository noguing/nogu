from typing import Optional

from fastapi import HTTPException
from odmantic import Model, Field

from models.user import User
from objects import glob


class OauthClient(Model):
    token: str = Field(primary_field=True)
    id: int
    username: str
    avatar_url: str

    async def save(self):
        await glob.db_oauth_clients.save(self)

    @staticmethod
    async def authorize_token(token: Optional[str]) -> User:
        if token is None:
            raise HTTPException(401)
        client = await glob.db_oauth_clients.find_one(OauthClient, OauthClient.token == token)
        if client is None:
            raise HTTPException(401)
        user = await glob.db_users.find_one(User, User.id == client.id)
        if user is None:
            raise HTTPException(401)
        return user


