import json
import pandas as pd
from jsonpath import jsonpath
from typing import Iterable, Hashable, Dict


def merge_to_dict(keys: Iterable[Hashable], values: Iterable, strict: bool = True):
    return {key: value for key, value in zip(keys, values, strict=strict)}


def dict_to_json(data: Dict, ensure_ascii=False, separators=(",", ":")):
    return json.dumps(data, ensure_ascii=ensure_ascii, separators=separators)


# save data to pd
def merge_data(data: list | dict, df: pd.DataFrame):
    if isinstance(data, list):
        tmp = pd.DataFrame(data)
    else:
        tmp = pd.DataFrame([data])
    result = pd.concat([df, tmp], ignore_index=True)
    return result


def json_parse(
    dict_obj: dict, target_keys: list | None = [], list_key_path: str | None = None
):
    # 列表页解析
    if list_key_path is not None:
        result = []
        element_list = jsonpath(dict_obj, list_key_path)
        if element_list:
            if element_list[0]:
                for element in element_list[0]:
                    item = {}
                    for key in target_keys:
                        value = jsonpath(element, f"$..{key}")
                        if value:
                            value = value[0]
                            item[key] = value
                        else:
                            print("key not find", key, element)
                    print(item)
                    result.append(item)
            return result
    # 单 dict 解析
    else:
        item = {}
        for key in target_keys:
            value = jsonpath(dict_obj, f"$..{key}")
            if value:
                value = value[0]
                item[key] = value
            else:
                print("key not find", key, dict_obj)
        return item
