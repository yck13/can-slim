from db.conn import get_client

def test_database_connection():
    client = get_client()
    assert client.server_info()