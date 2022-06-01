

from typing import Any, Dict, List, Optional, Type
from pydantic import BaseModel
import yaml
import sys
import json

from cli.formats.base import ListResponse, SingleResponse


class YamlListResponse(ListResponse):
    def print(self) -> None:
        yaml.dump(self.create_document(), sys.stdout)
    
    @staticmethod
    def create(title: Optional[str] = None) -> "YamlListResponse":
        return YamlListResponse(
            title="results" if title is None else title,
            entries=[])


class YamlSingleResponse(SingleResponse):
    def print(self) -> None:
        document = self.entry
        document = json.loads(document.json())
        yaml.dump(document, sys.stdout)
    
    @staticmethod
    def create(entry: BaseModel) -> "YamlSingleResponse":
        return YamlSingleResponse(entry=entry)
