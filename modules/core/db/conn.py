from pymongo import MongoClient
from pymongo.collection import Collection

from modules.core.util import config, log

_log = log.get_logger(__file__)

# get database collections
def get_stock_prices() -> Collection:
    return _db.stock_prices

# initialise connection below
_user = config.get('db.mongo.user')
_pass = config.get('db.mongo.pass')
_host = config.get('db.mongo.host')
_port = config.get('db.mongo.port')
_dbName = config.get('db.mongo.name')
_client = MongoClient('mongodb://{user}:{pw}@{host}:{port}/{dbName}'
                      .format(user=_user, pw=_pass, host=_host, port=_port, dbName=_dbName))
_db = _client[_dbName]

_client.server_info() # this line actually connects to database to test connection
_log.info('Connected to MongoDB')

