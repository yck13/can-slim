import mongomock
import pytest

import modules.core.db.access.stock as stock_dal
from modules.core.db.access.stock import list_stock_tickers, upsert_stocks, delete_stocks
from modules.core.model.stock import Stock


# replace actual reference with mock collection
@pytest.fixture(autouse=True)
def mock_collection():
    stock_dal._stock = mongomock.MongoClient().db.stock
    return stock_dal._stock


def test_list_stock_tickers(mock_collection):
    aapl = Stock(ticker='AAPL', name='Apple')
    mock_collection.insert_one(aapl._asdict())

    tickers = list_stock_tickers()
    assert tickers == ['AAPL']

def test_upsert_stocks(mock_collection):
    aapl_wrong = Stock(ticker='AAPL', name='Aaa')
    mock_collection.insert_many([aapl_wrong._asdict()])

    aapl = Stock(ticker='AAPL', name='Apple')
    goog = Stock(ticker='GOOG', name='Google')
    upsert_stocks([aapl, goog])

    docs = list(mock_collection.find())
    assert len(docs) == 2
    assert {'Apple', 'Google'} == {d['name'] for d in docs}


def test_delete_stocks(mock_collection):
    aapl = Stock(ticker='AAPL', name='Apple')
    goog = Stock(ticker='GOOG', name='Google')
    mock_collection.insert_many([aapl._asdict(), goog._asdict()])

    # delete google
    delete_stocks(['GOOG'])
    docs = list(mock_collection.find())
    assert len(docs) == 1
    assert docs[0]['ticker'] == 'AAPL'

    # delete apple
    delete_stocks(['AAPL'])
    docs = list(mock_collection.find())
    assert not docs
