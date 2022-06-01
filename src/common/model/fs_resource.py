


from ctypes import Union
from os import stat_result
from typing import Any, Dict, List, Optional
from pathlib import Path
from pathlib import PosixPath

from pydantic import BaseModel, Field

from common.model.file_info import FileInfo, StatCache
from common.model.storable import Storable


class FsResource(Storable):
    path: Path
    
    def no_longer_exists(self, cache: StatCache) -> bool:
        return cache.get_stat(Path(self.path)) is None
    
    def is_dirty(self, cache: StatCache) -> bool:
        raise Exception("Implement me")
    

class SingleFileResource(FsResource):
    info: FileInfo
    
    def is_dirty(self, cache: StatCache) -> bool:
        return self.info.is_dirty(cache)


class MultiFileResource(FsResource):
    infos: List[FileInfo]
    glob: str
    
    def files(self):
        yield from self.path.glob(self.path + self.glob)
    
    def contains(self, path: str) -> bool:
        for info in self.infos:
            if info.path == path:
                return True
        return False
        
    def is_dirty(self, cache: StatCache) -> bool:
        for info in self.infos:
            path = Path(info.path)
            if info.is_dirty(cache):
                return True
        path = Path(self.path)
        for child in self.files():
            if not self.contains(child):
                return True 
        return False

        
class SynchonizeResult(BaseModel):
    nb_deleted: int = 0
    nb_updated: int = 0
    nb_created: int = 0
    nb_unchanged: int = 0
    nb_errors: int = 0