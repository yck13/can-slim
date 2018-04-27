from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple

from modules.core.db.access.stock import list_stock_tickers, delete_stocks, upsert_stocks
from modules.core.log import get_logger
from modules.core.model.stock import Stock
from modules.core.util.list_util import set_difference
from modules.scraper.lse_scraper import LSEScraper, Index

_log = get_logger(__file__)
_SCRAPE_INDICES = [Index.FTSE100, Index.FTSE250]


def _scrape_constituents() -> List[Tuple[str, str]]:
    scraper = LSEScraper()
    all_constituents = []
    with ThreadPoolExecutor() as executor:
        futures = executor.map(scraper.get_constituents, _SCRAPE_INDICES)
        for stocks in futures:
            all_constituents.extend(stocks)
    return all_constituents


if __name__ == '__main__':
    # get new constituents list
    new_constituents = _scrape_constituents()

    # compare current db list with new list to find differences
    old_tickers = list_stock_tickers()
    new_tickers = [ticker for ticker, _ in new_constituents]
    _log.debug('Old tickers: {}'.format(old_tickers))
    _log.debug('New tickers: {}'.format(new_tickers))

    remove_tickers = set_difference(old_tickers, new_tickers)
    add_tickers = set_difference(new_tickers, old_tickers)
    _log.debug('Stocks to remove: {}'.format(remove_tickers))
    _log.debug('Stocks to add: {}'.format(add_tickers))

    ticker_name_lookup = {ticker: name for ticker, name in new_constituents}
    add_stocks = [Stock(ticker=ticker, name=ticker_name_lookup[ticker]) for ticker in add_tickers]

    # delete old and insert new entries to db
    delete_stocks(remove_tickers)
    _log.info('Removed old stock tickers')
    upsert_stocks(add_stocks)
    _log.info('Inserted new stock tickers nad names')

    _log.info('Stock list update complete')
