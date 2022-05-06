from datetime import datetime
from typing import List

from odmantic import Model, Reference, ObjectId

from models.user import User
from objects import glob


class Team(Model):
    name: str
    leader: User = Reference()
    creation_time: datetime
    users = List[ObjectId]

    async def save(self):
        await glob.db_teams.save(self)

    @staticmethod
    async def from_member(user_id: ObjectId) -> List['Team']:
        return await glob.db_teams.find(Team, user_id in Team.users)

