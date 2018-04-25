from modules.core.db.collection.stock import Stock


def list_stocks() -> [str]:
    return [s.ticker for s in Stock.objects.only('ticker')]
