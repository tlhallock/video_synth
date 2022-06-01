
from typing import Any, Dict, List
from pydantic import BaseModel

import json

class ListResponse(BaseModel):
    title: str
    entries: List[BaseModel]
    
    # TODO: Should be an iterator...
    def show(self, entries: List[BaseModel]) -> None:
        for entry in entries:
            self.add(entry)
        self.print()
    
    def add(self, entry: BaseModel) -> None:
        self.entries.append(entry)
    
    def create_document(self) -> Dict[str, Any]:
        return {self.title: [json.loads(e.json()) for e in self.entries]}
    
    def print(self) -> None:
        raise Exception("Not implemented")


class SingleResponse(BaseModel):
    entry: BaseModel
    
    def set(self, entry: BaseModel) -> None:
        self.entry = entry
    
    def print(self) -> None:
        raise Exception("Not implemented")
