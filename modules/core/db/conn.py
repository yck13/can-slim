from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from modules.core import config, log

_db: Database
_log = log.get_logger(__file__)


def get_collection(name: str) -> Collection:
    return _db.get_collection(name)


# initialise connection below
def init_connection() -> None:
    global _db
    user = config.get('db.mongo.user')
    password = config.get('db.mongo.pass')
    host = config.get('db.mongo.host')
    port = config.get('db.mongo.port')
    db_name = config.get('db.mongo.name')
    client = MongoClient('mongodb://{user}:{password}@{host}:{port}/{db_name}'
                         .format(user=user, password=password, host=host, port=port, db_name=db_name))
    _db = client[db_name]

    _db.list_collection_names()  # this line actually connects to database to test connection
    _log.info('Connected to MongoDB')


init_connection()
