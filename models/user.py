from odmantic import Model, Field

from objects import glob


class User(Model):
    id: int = Field(primary_field=True)
    username: str

    async def save(self):
        await glob.db_users.save(self)

