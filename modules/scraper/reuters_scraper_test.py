import pytest

from modules.scraper.reuters_scraper import ReutersScraper


@pytest.fixture
def scraper():
    return ReutersScraper()


def test_get_financials(scraper):
    financials = scraper.get_financials(ticker='HSBA.L')
    assert financials.growth_rates.eps_mrq_1yr_growth.company
    assert financials.growth_rates.eps_mrq_1yr_growth.industry
    assert financials.growth_rates.eps_mrq_1yr_growth.sector
    assert financials.growth_rates.eps_ttm_1yr_growth.company
    assert financials.growth_rates.eps_ttm_1yr_growth.industry
    assert financials.growth_rates.eps_ttm_1yr_growth.sector
