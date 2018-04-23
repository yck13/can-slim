import re

import requests
from bs4 import BeautifulSoup

from modules.core.model.index import Constituent
from modules.core.model.index import Index
from modules.core.util import config
from concurrent.futures import ThreadPoolExecutor

_CONSTITUENTS_URL = 'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/summary/' \
                    'summary-indices-constituents.html?index={index_ticker}&page={page}'


class LSEScraper:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=config.get('http.lse_scraper.parallelism'))

    def get_constituents(self, index: Index) -> [Constituent]:
        """
        scrapes and returns the list of underlying commpany tickers of index (e.g. UKX)
        :param index:
        :return:
        """

        def _open_page(page: int) -> str:
            url = _CONSTITUENTS_URL.format(index_ticker=index.ticker, page=page)
            response = requests.get(url)
            return response.content

        def _get_total_pages() -> int:
            html = _open_page(1)
            soup = BeautifulSoup(html, 'lxml')
            text = soup.select_one('#pi-colonna1-display > div:nth-of-type(1) > p.floatsx').text
            p = re.compile('Page 1 of (\d+)')
            m = p.search(text)
            return int(m.group(1))

        def _get_constituents_in_page(page: int) -> [Constituent]:
            html = _open_page(page)
            soup = BeautifulSoup(html, 'lxml')
            rows = soup.select('#pi-colonna1-display > table > tbody > tr')
            constituents = []
            for row in rows:
                [ticker, name, currency] = [cell.text.strip() for cell in row.find_all('td')[:3]]
                c = Constituent(ticker=ticker, name=name, currency=currency)
                constituents.append(c)
            return constituents

        total_pages = _get_total_pages()

        futures = [self.executor.submit(_get_constituents_in_page, page) for page in range(1, total_pages + 1)]
        constituents = [constituent for future in futures for constituent in future.result()]
        return constituents
