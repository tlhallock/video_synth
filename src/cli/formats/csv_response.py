
from typing import List, Optional, Type

import csv
from pydantic import BaseModel
import sys
from cli.formats.base import ListResponse


class CsvListResponse(ListResponse):
    keys: List[str]
    
    def print(self) -> None:
        writer = csv.DictWriter(sys.stdout, fieldnames=self.keys)
        writer.writeheader()
        
        for entry in self.entries:
            writer.writerow(entry.dict())

    @staticmethod
    def create(clazz: Type[BaseModel], title: Optional[str] = None) -> "CsvListResponse":
        schema = clazz.schema()
        return CsvListResponse(
            title=schema["title"] if title is None else title,
            keys=[key for key in schema["properties"].keys()],
            # titles=[val["title"] for val in schema["properties"].values()],
            # types=[val["type"] for val in schema["properties"].values()],
            entries=[],
        )
    

    

