from typing import NamedTuple, Optional

import requests
from bs4 import BeautifulSoup


class ReutersFinancialsDataPoint(NamedTuple):
    company: float
    industry: float
    sector: float


class ReutersGrowthRates(NamedTuple):
    eps_mrq_1yr_growth: ReutersFinancialsDataPoint  # most recent quarter
    eps_ttm_1yr_growth: ReutersFinancialsDataPoint  # trailing 12 months


class ReutersFinancials(NamedTuple):
    growth_rates: ReutersGrowthRates


class ReutersScraper:
    def get_financials(self, ticker: str) -> ReutersFinancials:
        """
        Returns the financials information given ticker
        :param ticker: e.g. HSBA.L
        :param country_code: e.g. uk
        :return:
        """
        EPS_MRQ_GROWTH_CSS_SELECTOR = '#content > div:nth-of-type(3) > div > div.sectionColumns > div.column1.gridPanel.grid8 > div:nth-of-type(8) > div.moduleBody > table > tbody > tr:nth-of-type(6)'
        EPS_TTM_GROWTH_CSS_SELECTOR = '#content > div:nth-of-type(3) > div > div.sectionColumns > div.column1.gridPanel.grid8 > div:nth-of-type(8) > div.moduleBody > table > tbody > tr:nth-of-type(7)'

        def open_page():
            url = 'https://www.reuters.com/finance/stocks/financial-highlights/{ticker}'.format(ticker=ticker)
            response = requests.get(url)
            return response.content

        def parse_html(html: str) -> ReutersFinancials:
            soup = BeautifulSoup(html, 'lxml')

            def extract_row(row_css_selector:str) -> (str, ReutersFinancialsDataPoint):
                row = soup.select_one(row_css_selector)
                cells = row.find_all('td')
                label = cells[0].text.strip()
                [company, industry, sector] = [ReutersScraper._str_to_float(cell.text) for cell in  cells[1:]]
                return (label, ReutersFinancialsDataPoint(company=company, industry=industry, sector=sector))

            (eps_mrq_label, eps_mrq_growth) = extract_row(EPS_MRQ_GROWTH_CSS_SELECTOR)
            assert eps_mrq_label == 'EPS (MRQ) vs Qtr. 1 Yr. Ago'

            (eps_ttm_label, eps_ttm_growth) = extract_row(EPS_TTM_GROWTH_CSS_SELECTOR)
            assert eps_ttm_label == 'EPS (TTM) vs TTM 1 Yr. Ago'

            return ReutersFinancials(
                growth_rates=ReutersGrowthRates(
                    eps_mrq_1yr_growth=eps_mrq_growth,
                    eps_ttm_1yr_growth=eps_ttm_growth
                )
            )

        html = open_page()
        financials = parse_html(html)
        return financials

    @staticmethod
    def _str_to_float(s: str) -> float:
        try:
            return float(s)
        except ValueError:
            return float('nan')
