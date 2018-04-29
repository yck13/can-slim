from datetime import datetime
from typing import NamedTuple, List


class HistoricDataPoint(NamedTuple):
    time: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

# type alias time series = list of historic data points
TimeSeries = List[HistoricDataPoint]

class Stock(NamedTuple):
    ticker: str
    name: str = None
    cusip: str = None
    sedol: str = None
    isin: str = None
    country_code: str = None
    time_series: TimeSeries = []
