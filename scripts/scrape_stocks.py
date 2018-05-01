from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
from timeit import default_timer as timer
from typing import List, Iterable

from modules.core.db.collections.stock_collection import list_stocks, upsert_stocks, delete_stocks
from modules.core.log import get_logger
from modules.core.model.stock import Stock
from modules.core.util.collections.list_util import set_difference
from modules.scraper.lse_scraper import LSEScraper, Index
from modules.scraper.market_watch_scraper import MarketWatchScraper

log = get_logger(__file__)
SCRAPE_TARGETS = [Index.FTSE100, Index.FTSE250]
SCRAPE_TARGETS_COUNTRY_CODE = 'UK'

lse_scraper = LSEScraper()
market_watch_scraper = MarketWatchScraper()


def get_current_tickers() -> List[str]:
    current_stocks = list_stocks(fields=['ticker'])
    return [s.ticker for s in current_stocks]


def scrape_new_tickers_from(indices: Iterable[Index]) -> List[str]:
    with ThreadPoolExecutor() as executor:
        futures = executor.map(lse_scraper.get_constituents, indices)
        tickers = [ticker for constituents in futures for ticker, _ in constituents]
    return tickers


def scrape_stock(ticker: str, country_code: str) -> Stock:
    basic_info = market_watch_scraper.get_basic_stock_info(ticker, country_code)
    time_series = market_watch_scraper.get_time_series(
        ticker=basic_info.ticker,
        country_code=basic_info.country_code,
        iso_code=basic_info.iso_code
    )
    quarterly_earnings = market_watch_scraper.get_quarterly_earnings(
        ticker=basic_info.ticker,
        country_code=basic_info.country_code,
        iso_code=basic_info.iso_code
    )
    log.debug('Scraped stock: {country_code}:{ticker}'.format(country_code=country_code, ticker=ticker))
    return Stock(
        ticker=ticker,
        name=basic_info.name,
        cusip=basic_info.cusip,
        sedol=basic_info.sedol,
        isin=basic_info.isin,
        country_code=country_code,
        time_series=time_series,
        quarterly_earnings=quarterly_earnings
    )


def insert_into_database(stock: Stock) -> None:
    upsert_stocks([stock])
    log.debug('Inserted into database: {}'.format(stock.ticker))


def scrape_stock_and_insert_into_database(ticker: str, country_code: str) -> None:
    try:
        stock = scrape_stock(ticker, country_code)
        insert_into_database(stock)
    except Exception:
        log.exception('Failed to scrape ticker: {}'.format(ticker))


def scrape_stocks_and_insert_into_database(tickers: Iterable[str], country_code: str) -> None:
    with ThreadPoolExecutor() as executor:
        futures = executor.map(scrape_stock_and_insert_into_database, tickers, repeat(country_code))

    # loop through lazy generator to make sure no exceptions are raised
    for _ in futures:
        pass


if __name__ == '__main__':
    start_time = timer()
    log.info('Started updating stock prices')
    current_tickers = get_current_tickers()

    log.info('Scraping new tickers from London Stock Exchange...')
    new_tickers = scrape_new_tickers_from(SCRAPE_TARGETS)
    log.info('Got new tickers: {}'.format(new_tickers))

    # delete obsolete tickers from database
    tickers_to_delete = set_difference(current_tickers, new_tickers)
    if tickers_to_delete:
        delete_stocks(tickers_to_delete)
        log.info('Deleted obsolete tickers: {}'.format(tickers_to_delete))

    scrape_stocks_and_insert_into_database(new_tickers, SCRAPE_TARGETS_COUNTRY_CODE)

    end_time = timer()
    log.info('Completed scraping {} stocks in {:.2f} seconds'.format(len(new_tickers), end_time - start_time))
