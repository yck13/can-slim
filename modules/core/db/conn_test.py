from modules.core.db.conn import _client

def test_database_connection():
    assert _client.server_info()