from mongoengine import connect

from modules.core import log, config

_log = log.get_logger(__file__)

# initialise connection below
_user = config.get('db.mongo.user')
_pass = config.get('db.mongo.pass')
_host = config.get('db.mongo.host')
_port = config.get('db.mongo.port')
_dbName = config.get('db.mongo.name')

_client = None


def start_connection():
    global _client
    _client = connect(db=_dbName, host=_host, port=_port, username=_user, password=_pass)
    _client.server_info()  # test database connection
    _log.info('Connected to MongoDB')
