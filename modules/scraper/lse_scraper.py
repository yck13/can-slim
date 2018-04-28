import re
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup

from modules.core import config

_CONSTITUENTS_URL = 'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/summary/' \
                    'summary-indices-constituents.html?index={index_ticker}&page={page}'


class Index(Enum):
    FTSE100 = ('UKX', 'L')
    FTSE250 = ('MCX', 'L')

    def __init__(self, index_ticker: str, suffix: str):
        self.index_ticker = index_ticker
        self.suffix = suffix


class LSEScraper:

    concurrency = config.get('scraper.lse.concurrency')

    def get_constituents(self, index: Index) -> List[Tuple[str, str]]:
        """
        scrapes and returns the list of (ticker, name) pairs
        :param index:
        :return:
        """

        def _open_page(page: int) -> str:
            url = _CONSTITUENTS_URL.format(index_ticker=index.index_ticker, page=page)
            response = requests.get(url)
            return response.content

        def _get_total_pages() -> int:
            html = _open_page(1)
            soup = BeautifulSoup(html, 'lxml')
            text = soup.select_one('#pi-colonna1-display > div:nth-of-type(1) > p.floatsx').text
            p = re.compile('Page 1 of (\d+)')
            m = p.search(text)
            return int(m.group(1))

        def _get_constituents_in_page(page: int) -> List[str]:
            html = _open_page(page)
            soup = BeautifulSoup(html, 'lxml')
            rows = soup.select('#pi-colonna1-display > table > tbody > tr')
            constituents = []
            for row in rows:
                [ticker, name] = [cell.text.strip() for cell in row.find_all('td')[:2]]
                ticker = _convert_to_yahoo_finance_ticker(ticker)
                constituent = (ticker, name)
                constituents.append(constituent)
            return constituents

        def _convert_to_yahoo_finance_ticker(ticker: str) -> str:
            if ticker.endswith('.'):
                ticker = ticker[:-1]
            ticker = ticker.replace('.', '-')
            return ticker + '.' + index.suffix

        total_pages = _get_total_pages()

        with ThreadPoolExecutor(max_workers=LSEScraper.concurrency) as executor:
            futures = executor.map(_get_constituents_in_page, range(1, total_pages + 1))
            constituents = [c for cs in futures for c in cs]
        return constituents
