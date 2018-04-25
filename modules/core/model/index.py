from enum import Enum
from typing import NamedTuple


# index enum
class Index(Enum):
    FTSE100 = 'UKX'
    FTSE250 = 'MCX'

    def __init__(self, ticker: str):
        self.ticker = ticker


# index constituent named tuple
IndexConstituent = NamedTuple('IndexConstituent', [
    ('ticker', str),
    ('name', str),
    ('currency', str)
])
