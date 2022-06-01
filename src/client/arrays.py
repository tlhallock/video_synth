from typing import Any, Dict, List

from cli.client.base import BaseClient

from common.model.array_info import (
    CreateArrayInfo,
    ArrayInfo,
    MatrixWriterGuard,
)


class ArraysClient(BaseClient[ArrayInfo]):
    def constructor(self, js: Dict[str, Any]) -> ArrayInfo:
        return ArrayInfo(**js)
    
    def create_array(self, args: CreateArrayInfo) -> ArrayInfo:
        return self.create(js=args.json())
    
    def open_array(self, args: CreateArrayInfo) -> MatrixWriterGuard:
        array = self.create_array(args)
        return array.open()
    
    def list_under_project(self, project: str) -> List[ArrayInfo]:
        override = f"projects/{project}/arrays"
        return self.list(override=override)
    
    def list_under_thing(self, thing: str) -> List[ArrayInfo]:
        override = f"things/{thing}/arrays"
        return self.list(override=override)
    
    @staticmethod
    def create_client() -> "ArraysClient":
        return ArraysClient(
            endpoint="http://localhost:5000",
            route="arrays",
        )
