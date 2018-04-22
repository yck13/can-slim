from pymongo import MongoClient
from pymongo.collection import Collection
import logging

from util import config, log

_logger = log.getLogger(__file__)

# get database collections
def get_stock_prices() -> Collection:
    return _db.stock_prices

def get_client() -> MongoClient:
    return client

# initialise connection below
_user = config.get('db.mongo.user')
_pass = config.get('db.mongo.pass')
_host = config.get('db.mongo.host')
_port = config.get('db.mongo.port')
_dbName = config.get('db.mongo.name')
client = MongoClient('mongodb://{user}:{pw}@{host}:{port}/{dbName}'
                     .format(user=_user, pw=_pass, host=_host, port=_port, dbName=_dbName))
_db = client[_dbName]

client.server_info()
_logger.info('Connected to MongoDB')

