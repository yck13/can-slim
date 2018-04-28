from concurrent.futures import ThreadPoolExecutor
from typing import List, Generator
from timeit import default_timer as timer

from modules.core.db.collections.stock_collection import list_stocks, upsert_stocks, delete_stocks
from modules.core.log import get_logger
from modules.core.model.stock import Stock
from modules.core.util.collections.list_util import set_difference
from modules.scraper.alpha_vantage_scraper import AlphaVantageScraper
from modules.scraper.lse_scraper import LSEScraper, Index

log = get_logger(__file__)

lse_scraper = LSEScraper()
alpha_vantage_scraper = AlphaVantageScraper()

# custom types
StocksGenerator = Generator[Stock, None, None]


def get_current_tickers() -> List[str]:
    current_stocks = list_stocks(fields=['ticker'])
    return [s.ticker for s in current_stocks]


def scrape_new_tickers_from(*indices: Index) -> List[str]:
    with ThreadPoolExecutor() as executor:
        futures = executor.map(lse_scraper.get_constituents, indices)
        tickers = [ticker for constituents in futures for ticker, _ in constituents]
    return tickers


def scrape_stock(ticker: str) -> Stock:
    time_series = alpha_vantage_scraper.get_time_series(ticker)
    log.debug('Scraped stock: {}'.format(ticker, time_series))
    return Stock(ticker=ticker, time_series=time_series)


def insert_into_database(stock: Stock) -> None:
    upsert_stocks([stock])
    log.debug('Inserted into database: {}'.format(stock.ticker))


def scrape_stock_and_insert_into_database(ticker: str) -> None:
    stock = scrape_stock(ticker)
    insert_into_database(stock)


if __name__ == '__main__':
    start_time = timer()
    log.info('Started updating stock prices')
    current_tickers = get_current_tickers()

    log.info('Scraping new tickers from London Stock Exchange...')
    new_tickers = scrape_new_tickers_from(Index.FTSE100, Index.FTSE250)
    log.info('Got new tickers: {}'.format(new_tickers))

    # delete obsolete tickers from database
    tickers_to_delete = set_difference(current_tickers, new_tickers)
    if tickers_to_delete:
        delete_stocks(tickers_to_delete)
        log.info('Deleted obsolete tickers: {}'.format(tickers_to_delete))

    with ThreadPoolExecutor() as executor:
        executor.map(scrape_stock_and_insert_into_database, new_tickers)

    end_time = timer()
    log.info('Completed update stock prices in {:.2f} seconds', end_time - start_time)
