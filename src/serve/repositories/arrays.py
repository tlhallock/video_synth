
from typing import Any, Dict

from pathlib import Path
from common.model.array_info import ArrayInfo

import serve.database as db
from serve.repositories.fs_repo import FileSystemRepo
from src.common.model.file_info import StatCache

# These should be deleted when the project is deleted...

class ArraysRepository(FileSystemRepo[ArrayInfo]):
    def __init__(self) -> None:
        super().__init__(
            collection=db.thing_collection,
            desc="thing")
    
    def construct(self, data: Dict[str, Any]) -> ArrayInfo:
        id = data["_id"]
        del data["_id"]
        return ArrayInfo(**data, id=id)
    
    def create_document(self, path: Path, cache: StatCache) -> ArrayInfo:
        return ArrayInfo.create_document(path, cache)
    

repository: ArraysRepository = ArraysRepository()
