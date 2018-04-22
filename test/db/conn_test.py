from db.conn import get_database

def test_database_connection():
    assert get_database() is not None