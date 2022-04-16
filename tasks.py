import json

from huey import SqliteHuey
from ossapi import serialize_model, Beatmap

from objects import glob
from objects.glob import mongo_db_sync

huey = SqliteHuey(filename="huey.db")


@huey.task(retries=2, retry_delay=4)
def gather_beatmap(beatmap_id: int):
    beatmap: Beatmap = glob.osu_api.beatmap(beatmap_id).expand()
    beatmap_json = json.loads(serialize_model(beatmap))
    beatmap_set_json = json.loads(serialize_model(beatmap.beatmapset()))
    mongo_db_sync['beatmap'].update_one({"id": beatmap.id},
                                        {"$set": beatmap_json},
                                        upsert=True)
    mongo_db_sync['beatmap_set'].update_one({"id": beatmap.beatmapset_id},
                                            {"$set": beatmap_set_json},
                                            upsert=True)
