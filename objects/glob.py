import json
import os

from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from ossapi import OssapiV2
from pymongo.database import Database


def read_config(content: str) -> dict:
    return json.load(open(f"{os.getcwd()}\config.json", 'r'))[content]


def get_url(path: str) -> str:
    return f"http{'s' if config_app['https'] else ''}://{config_app['domain']}/{path}"


def get_db(database: str):
    return AIOEngine(motor_client, database)


config_app = read_config('app')
config_mongo = read_config('mongo')
config_oauth = read_config('oauth')
config_proxy = read_config('proxy')

motor_client: Database = AsyncIOMotorClient(config_mongo['host'], config_mongo['port'])[config_mongo['database']]

osu_api = OssapiV2(config_oauth['client_id'], config_oauth['client_secret'])

db_oauth_clients = get_db('oauth_clients')
db_users = get_db('users')
db_teams = get_db('teams')
