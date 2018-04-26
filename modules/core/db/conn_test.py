from modules.core.db.conn import _db

def test_connection():
    assert _db.list_collection_names()