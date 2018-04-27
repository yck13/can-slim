from modules.core.db.access import stock
from modules.core.log import get_logger

_log = get_logger(__file__)

if __name__ == '__main__':
    stock.create_indexes()
    _log.info('Create DB indexes complete')
