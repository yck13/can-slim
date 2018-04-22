import config
from pymongo import MongoClient


def get_historic_prices():
    return db.historic_prices


def get_database():
    return db

[_user, _pass, _host, _port, _dbName] = [config.get('db.mongo.{}'.format(v)) for v in ['user', 'pass', 'host', 'port', 'database']]

_client = MongoClient('mongodb://{}:{}@{}/{}'.format(_user, _pass, _host, _port))
db = _client[_dbName]
