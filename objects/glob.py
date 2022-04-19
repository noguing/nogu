import json

from motor.motor_asyncio import AsyncIOMotorClient
from ossapi import OssapiV2
from pymongo.database import Database


def read_config(content: str) -> dict:
    return json.load(open("config.json", 'r'))[content]


config_mongo = read_config("mongo")
config_oauth = read_config("oauth")

osu_api = OssapiV2(config_oauth['client_id'], config_oauth['client_secret'])

mongo_db: Database = AsyncIOMotorClient(config_mongo['host'], config_mongo['port'])[config_mongo['database']]
db_beatmap = mongo_db['beatmap']
