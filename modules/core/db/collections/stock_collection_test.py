from datetime import datetime

import mongomock
import pytest

from modules.core.db.collections import stock_collection
from modules.core.db.collections.stock_collection import list_stocks, upsert_stocks, delete_stocks
from modules.core.model.stock import Stock, HistoricDataPoint, EarningsEvent


@pytest.fixture(autouse=True)
def mock_collection():
    stock_collection._collection = mongomock.MongoClient().db.stock
    return stock_collection._collection


def test_list_stocks(mock_collection):
    aapl = Stock(
        ticker='AAPL',
        name='Apple',
        time_series=[HistoricDataPoint(time=datetime(2001, 1, 1), open=1, high=1, low=1, close=1, volume=100)],
        quarterly_earnings=[EarningsEvent(time=datetime(2001, 1, 1), value=10)]
    )
    aapl_dict = {
        'ticker': 'AAPL',
        'name': 'Apple',
        'time_series': [{'time': datetime(2001, 1, 1), 'open': 1, 'high': 1, 'low': 1, 'close': 1, 'volume': 100}],
        'quarterly_earnings': [{'time': datetime(2001, 1, 1), 'value': 10}]
    }
    mock_collection.insert_one(aapl_dict)

    stocks = list_stocks(fields=[])
    assert stocks == [aapl]


def test_upsert_stocks(mock_collection):
    aapl_wrong = Stock(ticker='AAPL', name='Aaa')
    mock_collection.insert_many([aapl_wrong._asdict()])

    aapl = Stock(
        ticker='AAPL',
        name='Apple',
        time_series=[HistoricDataPoint(time=datetime(2001, 1, 1), open=1, high=1, low=1, close=1, volume=100)],
        quarterly_earnings=[EarningsEvent(time=datetime(2001, 1, 1), value=10)]
    )
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
