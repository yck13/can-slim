from typing import TypeVar, List

T = TypeVar('T')

def set_difference(left: List[T], right: List[T]) -> List[T]:
    return list(set(left) - set(right))