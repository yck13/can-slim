from os.path import join
from typing import Dict

from ruamel.yaml import YAML

from constants import PROJECT_ROOT


def get(key: str) -> object:
    """
    dot based accessor for nested key, e.g. 'db.mongo.user'
    :param key:
    :return:
    """
    d = _config
    iter_keys = key.split('.')
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
