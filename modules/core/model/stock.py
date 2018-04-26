from datetime import date
from typing import NamedTuple, List, Optional


class HistoricPrice(NamedTuple):
    date: date
    price: float


class Stock(NamedTuple):
    ticker: str
    name: str
    historicPrices: List[HistoricPrice] = []
