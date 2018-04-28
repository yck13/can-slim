from typing import List, Dict, Iterable

from pymongo import ReplaceOne, IndexModel, ASCENDING
from datetime import datetime, time
from modules.core.db.conn import get_collection
from modules.core.model.stock import Stock, HistoricDataPoint

# database stock collections
_collection = get_collection('stock')


def _document_to_stock(document: Dict) -> Stock:
    document.pop('_id', None)
    if 'time_series' in document:
        document['time_series'] = [HistoricDataPoint(**pt) for pt in document['time_series']]
    stock = Stock(**document)
    return stock

def list_stocks(fields: List[str] = []) -> List[Stock]:
    args = {}
    if fields:
        args['projection'] = {field: True for field in fields}
    cursor = _collection.find(**args)
    return [_document_to_stock(doc) for doc in cursor]


def upsert_stocks(stocks: Iterable[Stock]) -> None:
    if not stocks:
        return
    requests = [ReplaceOne(filter={'ticker': s.ticker}, replacement=s._asdict(), upsert=True) for s in stocks]
    return _collection.bulk_write(requests)


def delete_stocks(tickers: Iterable[str]) -> None:
    if not tickers:
        return
    return _collection.delete_many(filter={'ticker': {'$in': list(tickers)}})


def create_indexes() -> None:
    ticker_ts_index = IndexModel([('ticker', ASCENDING), ('time_series.time', ASCENDING)], unique=True)
    _collection.create_indexes([ticker_ts_index])
