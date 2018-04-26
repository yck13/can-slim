from concurrent.futures import ThreadPoolExecutor
from typing import List

from modules.core.db.access.stock import list_stock_tickers, delete_stocks, upsert_stocks
from modules.core.log import get_logger
from modules.core.model.index import Index
from modules.core.model.stock import Stock
from modules.core.util.list_util import set_difference
from modules.scraper.lse_scraper import LSEScraper

_log = get_logger(__file__)
_SCRAPE_INDICES = [Index.FTSE100, Index.FTSE250]


def _scrape_stock_tickers() -> List[str]:
    scraper = LSEScraper()
    tickers = []
    with ThreadPoolExecutor() as executor:
        futures = executor.map(scraper.get_constituents, _SCRAPE_INDICES)
        for index_tickers in futures:
            tickers.extend(index_tickers)
    return tickers


def run_script():
    old_tickers = list_stock_tickers()
    new_tickers = _scrape_stock_tickers()
    _log.debug('Old tickers: {}'.format(old_tickers))
    _log.debug('New tickers: {}'.format(new_tickers))

    remove_tickers = set_difference(old_tickers, new_tickers)
    _log.debug('Stocks to remove: {}'.format(remove_tickers))

    add_tickers = set_difference(new_tickers, old_tickers)
    add_stocks = [Stock(ticker=ticker) for ticker in add_tickers]
    _log.debug('Stocks to add: {}'.format(add_tickers))

    delete_stocks(remove_tickers)
    _log.info('Removed old stock tickers')
    upsert_stocks(add_stocks)
    _log.info('Inserted new stock tickers')

    _log.info('Stock list update complete')


if __name__ == '__main__':
    run_script()
