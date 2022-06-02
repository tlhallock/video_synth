

from os import stat_result
from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar
from pathlib import Path

import pymongo

from common.model.base import BaseModel
from common.utils.utils import get_time, create_uuid
from serve.exceptions import NotFoundException
from common.schema.updates import JsonUpdates
from serve.repositories.base import BaseRepository

from common.model.file_info import FileInfo, StatCache
from common.model.fs_resource import SynchonizeResult, FsResource


# Perhaps delete should remove from the filesystem as well?



T = TypeVar('T', bound=FsResource)
class FileSystemRepo(BaseRepository[T]):
    root: Path
    globs: List[str]
    
    def __init__(self, database, desc: str, root: Path, globs: List[str]):
        super().__init__(database, desc)
        self.root = root
        self.globs = globs
    
    def create_document(self, path: Path, cache: StatCache) -> None:
        raise Exception()
    
    def _update_document(self, document: T, sync: SynchonizeResult) -> None:
        cache = StatCache()
        if document.no_longer_exists(cache):
            self.delete(document)
            sync.nb_deleted += 1
            return
            
        if not document.is_dirty(cache):
            sync.nb_unchanged += 1
            return
        
        new_document = self.create_document(document.path, cache)
        new_document.as_updates(document)
        result = self.save(new_document)
        
        # updates = new_document.dict()
        # updates["updated"] = get_time()
        # result = self.collection.update_one({"_id": id}, {"$set": updates})
        # if not result.modified_count:
        if result is not None:
            print(f"Unable to update {self.desc} {id}")
            sync.nb_errors += 1
            return
        
        sync.nb_updated += 1
    
    def update_existing(self, sync: SynchonizeResult) -> None:
        for document in self.find_by({}):
            self._update_document(document, sync)
            
    def scan(self, sync: SynchonizeResult) -> None:
        for glob in self.globs:
            for child in self.root.rglob(glob):
                document = self.find_one_by({
                    "path": {"$eq": str(child)}
                })
                # res = self.get_collection().count(
                #     {"path": {"$eq": str(child) }},
                #     {"limit": 1}
                # )
                # print(child)
                # print(document)
                if document is not None:
                    continue
                
                created = self.create_document(child, StatCache())
                # print("created", created)
                # import pdb; pdb.set_trace()
                result = self.save(created)
                assert result.inserted_id is not None
                sync.nb_created += 1
        
    def synchronize(self) -> SynchonizeResult:
        result = SynchonizeResult()
        self.update_existing(result)
        self.scan(result)
        return result
    
    def synchronize_entry(self, id: str) -> SynchonizeResult:
        result = SynchonizeResult()
        document = self.find_one_by_id(id)
        if not document:
            raise NotFoundException(id)
        self._update_document(document=document, sync=result)
        return result
            
            
            
            