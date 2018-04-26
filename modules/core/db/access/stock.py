from typing import List

from pymongo import ReplaceOne
from pymongo.results import BulkWriteResult, DeleteResult

from modules.core.db.conn import get_collection
from modules.core.model.stock import Stock

# Data access layer for Stock

_stock = get_collection('stock')


def list_stock_tickers() -> List[str]:
    return [doc['ticker'] for doc in _stock.find(projection={'_id': False, 'ticker': True})]


def upsert_stocks(stocks: List[Stock]) -> None:
    if not stocks:
        return
    requests = [ReplaceOne(filter={'ticker': s.ticker}, replacement=s._asdict(), upsert=True) for s in stocks]
    return _stock.bulk_write(requests)


def delete_stocks(tickers: List[str]) -> None:
    if not tickers:
        return
    return _stock.delete_many(filter={'ticker': {'$in': tickers}})
