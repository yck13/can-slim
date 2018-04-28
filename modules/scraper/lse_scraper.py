import re
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from typing import List, Tuple, NamedTuple

import requests
from bs4 import BeautifulSoup

from modules.core import config


class Index(Enum):
    FTSE100 = 'UKX'
    FTSE250 = 'MCX'

    def __init__(self, index_ticker: str):
        self.index_ticker = index_ticker

class IndexConstituent(NamedTuple):
    ticker: str
    name: str

class LSEScraper:
    concurrency = config.get('scraper.lse.concurrency')

    def get_constituents(self, index: Index) -> List[IndexConstituent]:
        """
        scrapes and returns the list of (ticker, name) pairs
        :param index:
        :return:
        """

        def open_page(page: int) -> str:
            url = 'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/summary/' \
                  'summary-indices-constituents.html?index={index_ticker}&page={page}' \
                .format(index_ticker=index.index_ticker, page=page)
            response = requests.get(url)
            return response.content

        def get_total_pages() -> int:
            html = open_page(1)
            soup = BeautifulSoup(html, 'lxml')
            text = soup.select_one('#pi-colonna1-display > div:nth-of-type(1) > p.floatsx').text
            p = re.compile('Page 1 of (\d+)')
            m = p.search(text)
            return int(m.group(1))

        def get_constituents_in_page(page: int) -> List[str]:
            html = open_page(page)
            soup = BeautifulSoup(html, 'lxml')
            rows = soup.select('#pi-colonna1-display > table > tbody > tr')
            constituents = []
            for row in rows:
                [ticker, name] = [cell.text.strip() for cell in row.find_all('td')[:2]]
                constituent = IndexConstituent(ticker=ticker, name=name)
                constituents.append(constituent)
            return constituents

        total_pages = get_total_pages()

        with ThreadPoolExecutor(max_workers=LSEScraper.concurrency) as executor:
            futures = executor.map(get_constituents_in_page, range(1, total_pages + 1))
            constituents = [c for cs in futures for c in cs]
        return constituents
