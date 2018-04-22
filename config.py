from os.path import dirname, abspath, join
from typing import Dict

from ruamel.yaml import YAML

PROJECT_ROOT: str = dirname(abspath(__file__))

def get(key: str) -> object:
    """
    dot based accessor for nested key, e.g. 'db.mongo.user'
    :param key:
    :return:
    """
    iter_keys = key.split('.')
    d = _config
    try:
        for k in iter_keys:
            d = d[k]
    except KeyError:
        raise KeyError("'{}' is not present in config".format(key))
    else:
        return d

with open(join(PROJECT_ROOT, 'config.yml')) as f:
    _yaml = YAML(typ='safe')
    _config: Dict = _yaml.load(f)
