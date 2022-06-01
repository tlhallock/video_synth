
from datetime import datetime
from typing import Any, Dict, List, Optional, Type
from pydantic import BaseModel
# import orjson
import json

import sys

from cli.formats.base import ListResponse, SingleResponse
from cli.utils import my_default


# class MyEncoder(json.JSONEncoder):
#     def __init__(self, *args, **kwargs) -> None:
#         super().__init__(*args, **kwargs, sort_keys=True, indent=True)
        
#     def default(self, obj):
#         if isinstance(obj, datetime):
#             return str(obj)
#         # Let the base class default method raise the TypeError
#         return json.JSONEncoder.default(self, obj)


def my_big_fat_dump(obj):
    json.dump(
        obj,
        sys.stdout,
        indent=2,
        sort_keys=True,
        # default=my_default
    )


class JsonListResponse(ListResponse):
    def print(self) -> None:
        my_big_fat_dump(self.create_document())
    
    @staticmethod
    def create(title: Optional[str] = None) -> "JsonListResponse":
        return JsonListResponse(
            title="results" if title is None else title,
            entries=[])


class JsonSingleResponse(SingleResponse):
    def print(self) -> None:
        # print(self.entry.dict())
        doc = json.loads(self.entry.json())
        my_big_fat_dump(doc)
    
    @staticmethod
    def create(entry: BaseModel) -> "JsonSingleResponse":
        return JsonSingleResponse(entry=entry)
