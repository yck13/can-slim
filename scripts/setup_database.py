from modules.core.db.collections.stock_collection import create_indexes
from modules.core.log import get_logger

log = get_logger(__file__)

if __name__ == '__main__':
    create_indexes()
    log.info('Created database indices')
