
from typing import List, Optional, Type

from rich.table import Table
from rich.console import Console
from pydantic import BaseModel

from cli.formats.base import ListResponse


def to_str(val, val_type):
    return str(val)


class RichListResponse(ListResponse):
    keys: List[str]
    titles: List[str]
    types: List[str]
    
    def print(self) -> None:
        table = Table(title=self.title)
        for title in self.titles:
            table.add_column(
                title,
                style="cyan",
                justify="center",
                overflow="fold",
            )
            # no_wrap=True, 
        
        for entry in self.entries:
            d = entry.dict()
            table.add_row(*[
                to_str(d[key], val_type)
                for key, val_type in zip(self.keys, self.types)
            ])
        
        console = Console()
        console.print(table)

    @staticmethod
    def create(clazz: Type[BaseModel], title: Optional[str] = None) -> "RichListResponse":
        schema = clazz.schema()
        return RichListResponse(
            title=schema["title"] if title is None else title,
            keys=[key for key in schema["properties"].keys()],
            titles=[val["title"] if "title" in val else key for key, val in schema["properties"].items()],
            types=[val["type"] if "type" in val else "unknown" for val in schema["properties"].values()],
            entries=[],
        )
    

    

