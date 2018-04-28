import json
from datetime import datetime
from typing import List

import requests

from modules.core import config
from modules.core.model.stock import TimeSeries, HistoricDataPoint
from pandas import to_datetime


class MarketWatchScraper:
    ckey = config.get('scraper.market_watch.ckey')
    entitlement_token = config.get('scraper.market_watch.entitlement_token')
    default_step = config.get('scraper.market_watch.step')
    default_timeframe = config.get('scraper.market_watch.timeframe')

    def get_time_series(self, ticker: str, step: str = default_step, timeframe: str = default_timeframe) -> TimeSeries:
        """
        Returns time series for ticker (e.g. HSBA) given step and timeframe
        :param ticker:
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
                        'Key': ticker,
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
                time=to_datetime(unix_timestamp, unit='ms').to_pydatetime(),
                open=open,
                high=high,
                low=low,
                close=last,
                volume=volume
            ) for unix_timestamp, [open, high, low, last], [volume] in zip(time_axis, price_series, volume_series)]
            return time_series

        response = open_page()
        time_series = parse_response(response)
        return time_series
