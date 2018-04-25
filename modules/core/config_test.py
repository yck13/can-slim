import pytest

from modules.core import config


def test_get():
    mongo_config = config.get('db.mongo')
    assert 'host' in mongo_config
    assert 'port' in mongo_config
    assert 'user' in mongo_config
    assert 'pass' in mongo_config
    assert 'name' in mongo_config


def test_get_error():
    with pytest.raises(KeyError):
        config.get('random.key')
