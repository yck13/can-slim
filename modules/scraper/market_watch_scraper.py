import json
from typing import List, NamedTuple
from warnings import warn, simplefilter

import requests
from pandas import to_datetime

from modules.core import config
from modules.core.model.stock import TimeSeries, HistoricDataPoint, EarningsEvent


class BasicStockInfo(NamedTuple):
    ticker: str
    name: str
    cusip: str
    sedol: str
    isin: str
    country_code: str
    iso_code: str


class MarketWatchScraper:
    ckey = config.get('scraper.market_watch.ckey')
    entitlement_token = config.get('scraper.market_watch.entitlement_token')
    default_step = config.get('scraper.market_watch.step')
    default_timeframe = config.get('scraper.market_watch.timeframe')

    def get_basic_stock_info(self, ticker: str, country_code: str) -> BasicStockInfo:
        """
        Returns the basic stock information for a ticker and country code (e.g. common name, cusip, isin...)
        :param ticker: e.g. HSBA
        :param country_code: e.g. uk
        :return:
        """

        def open_page():
            url = 'https://api.wsj.net/api/dylan/quotes/v2/comp/quote'
            params = {
                'needed': 'TradingRange|Meta',
                'id': '{ticker}|{country_code}|||'.format(ticker=ticker, country_code=country_code),
                'maxInstrumentMatches': 1,
                'ckey': MarketWatchScraper.ckey,
                'EntitlementToken': MarketWatchScraper.entitlement_token,
                'accept': 'application/json'
            }
            response = requests.get(url, params)
            return response.content

        def parse_response(response_json: str) -> BasicStockInfo:
            data = json.loads(response_json)
            instrument = data['GetInstrumentResponse']['InstrumentResponses'][0]['Matches'][0]['Instrument']
            return BasicStockInfo(
                ticker=instrument['Ticker'],
                name=instrument['CommonName'],
                cusip=instrument['Cusip'],
                sedol=instrument['Sedol'],
                isin=instrument['Isin'],
                country_code=instrument['Exchange']['CountryCode'],
                iso_code=instrument['Exchange']['IsoCode']
            )

        response = open_page()
        basic_stock_info = parse_response(response)
        return basic_stock_info

    def get_time_series(self, ticker: str, country_code: str, iso_code: str, step: str = default_step,
                        timeframe: str = default_timeframe) -> TimeSeries:
        """
        Returns time series for ticker (e.g. HSBA) given step and timeframe
        :param ticker: e.g. HSBA
        :param country_code: for ticker, e.g. uk
        :param iso_code: for ticker, e.g. xlon
        :param step: e.g. P1D for daily, if not supplied default will be used
        :param timeframe: e.g. P5Y for 5 years, if not supplied default will be used
        :return:
        """
        PRICE_SERIES_ID = 'price'
        VOLUME_SERIES_ID = 'volume'

        def open_page() -> str:
            url = 'https://api-secure.wsj.net/api/michelangelo/timeseries/history'
            options = {
                'Step': step,
                'TimeFrame': timeframe,
                'EntitlementToken': MarketWatchScraper.entitlement_token,
                'Series': [
                    {
                        'Key': 'STOCK/{country_code}/{iso_code}/{ticker}'.format(country_code=country_code,
                                                                                 iso_code=iso_code, ticker=ticker),
                        'Dialect': 'Charting',
                        'Kind': 'Ticker',
                        'SeriesId': PRICE_SERIES_ID,
                        'DataTypes': ['Open', 'High', 'Low', 'Last'],
                        'Indicators': [
                            {'Parameters': [], 'Kind': 'Volume', 'SeriesId': VOLUME_SERIES_ID}
                        ]
                    }
                ]
            }
            params = {
                'json': json.dumps(options),
                'ckey': MarketWatchScraper.ckey
            }
            headers = {
                'Dylan2010.EntitlementToken': MarketWatchScraper.entitlement_token
            }
            response = requests.get(url, params, headers=headers)
            return response.content

        def parse_response(response_json: str) -> TimeSeries:
            data = json.loads(response_json)

            def extract_series(series_id: str) -> List[List[float]]:
                return next(s['DataPoints'] for s in data['Series'] if s['SeriesId'] == series_id)

            time_axis = data['TimeInfo']['Ticks']
            price_series = extract_series(PRICE_SERIES_ID)
            volume_series = extract_series(VOLUME_SERIES_ID)
            time_series = [HistoricDataPoint(
                time=MarketWatchScraper._unix_to_datetime(unix_timestamp),
                open=open,
                high=high,
                low=low,
                close=last,
                volume=volume
            ) for unix_timestamp, [open, high, low, last], [volume]
                in zip(time_axis, price_series, volume_series)]
            return time_series

        response = open_page()
        time_series = parse_response(response)
        return time_series

    def get_quarterly_earnings(self, ticker: str, country_code: str, iso_code: str,
                               timeframe: str = default_timeframe) -> List[EarningsEvent]:
        """
        Returns quarterly earnings series for ticker (e.g. HSBA) given step and timeframe
        :param ticker: e.g. HSBA
        :param country_code: for ticker, e.g. uk
        :param iso_code: for ticker, e.g. xlon
        :param timeframe: e.g. P5Y for 5 years, if not supplied default will be used
        :return:
        """
        simplefilter('always', DeprecationWarning)
        warn("This method is deprecated as data is missing for many UK stocks", DeprecationWarning)

        EARNINGS_SERIES_ID = 'earnings'

        def open_page() -> str:
            url = 'https://api-secure.wsj.net/api/michelangelo/timeseries/history'
            options = {
                'Step': 'P10Y',
                # since we are only interested in events, we try to get rid of irrelevant series data by using a large step
                'TimeFrame': timeframe,
                'EntitlementToken': MarketWatchScraper.entitlement_token,
                'Series': [
                    {
                        'Key': 'STOCK/{country_code}/{iso_code}/{ticker}'.format(country_code=country_code,
                                                                                 iso_code=iso_code, ticker=ticker),
                        'Dialect': 'Charting',
                        'Kind': 'Ticker',
                        'SeriesId': 's1',
                        'Indicators': [
                            {
                                'Parameters': [{'Name': 'YearOverYear'}],
                                'Kind': 'EarningsEvents',
                                'SeriesId': EARNINGS_SERIES_ID
                            }
                        ]
                    }
                ]
            }
            params = {
                'json': json.dumps(options),
                'ckey': MarketWatchScraper.ckey
            }
            headers = {
                'Dylan2010.EntitlementToken': MarketWatchScraper.entitlement_token
            }
            response = requests.get(url, params, headers=headers)
            return response.content

        def parse_response(response_json: str) -> List[EarningsEvent]:
            data = json.loads(response_json)
            events = data['Events'][0]['DataPoints']
            quarterly_earnings = [EarningsEvent(
                time=MarketWatchScraper._unix_to_datetime(event['EventDate']),
                value=event['Value']
            ) for event in events]
            return quarterly_earnings

        response = open_page()
        time_series = parse_response(response)
        return time_series

    def get_annual_earnings(self, ticker: str, country_code: str):
        pass

    @staticmethod
    def _unix_to_datetime(millis: int):
        return to_datetime(millis, unit='ms').to_pydatetime()
