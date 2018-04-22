import logging
from logging import DEBUG, INFO, WARN, WARNING, ERROR, FATAL, Logger
from util import config

def getLogger(name: str) -> Logger:
    logger = logging.getLogger(name)
    logger.setLevel(DEBUG)
    logger.addHandler(_ch)
    return logger

def _getLogLevelFromConfig():
    lookup = {
        'debug': DEBUG,
        'info': INFO,
        'warn': WARN,
        'warning': WARNING,
        'error': ERROR,
        'fatal': FATAL
    }
    fallback = DEBUG
    try:
        level = config.get('log.level')
    except KeyError:
        return fallback
    else:
        return lookup.get(str(level).lower(), fallback)

# create console handler
_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
_level = _getLogLevelFromConfig()
_ch = logging.StreamHandler()
_ch.setFormatter(_formatter)
_ch.setLevel(_level)
