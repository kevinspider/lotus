from typing import Iterable, Hashable


def merge_to_dict(keys: Iterable[Hashable], values: Iterable, strict:bool = True):
    return {key: value for key, value in zip(keys, values, strict=strict)}