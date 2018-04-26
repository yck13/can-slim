from datetime import date
from typing import NamedTuple, List, Optional


class HistoricDataPoint(NamedTuple):
    date: date
    price: float
    volume: float

# type alias time series = list of historic data points
TimeSeries = List[HistoricDataPoint]

class Stock(NamedTuple):
    ticker: str
    name: str = None
    time_series: TimeSeries = []
