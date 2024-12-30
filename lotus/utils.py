import json
from typing import Iterable, Hashable, Dict


def merge_to_dict(keys: Iterable[Hashable], values: Iterable, strict:bool = True):
    return {key: value for key, value in zip(keys, values, strict=strict)}

def dict_to_json(data: Dict, ensure_ascii=False, separators=(',', ':')):
    return json.dumps(data, ensure_ascii=ensure_ascii, separators=separators)


