from itertools import islice
from typing import TypeVar, Iterable

T = TypeVar('T')


def chunks(iterable: Iterable[T], chunk_size: int):
    """
    Lazily split iterable into n sized chunks
    :param iterable:
    :param chunk_size:
    :return:
    """
    iterable = iter(iterable)
    while True:
        x = tuple(islice(iterable, chunk_size))
        if not x:
            return
        yield x
