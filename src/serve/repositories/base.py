

from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar
from bson import ObjectId

import pymongo

from common.model.base import BaseModel
from common.utils.utils import get_time, create_uuid
from serve.exceptions import NotFoundException
from common.schema.updates import JsonUpdates
from common.model.storable import Storable
from pydantic_mongo import AbstractRepository, ObjectIdField

from src.common.model.search import Search


T = TypeVar('T', bound=Storable)

class BaseRepository(AbstractRepository[T]):
    desc: str
    
    def __init__(self, database, desc: str):
        super().__init__(database)
        self.desc = desc
    
    def list(self, filters: Optional[Dict] = None) -> List[T]:
        if filters is None:
            return list(self.find_by({}))
        else:
            return list(self.find_by(filters))
    
    def create(self, document: T) -> T:
        result = self.save(document)
        assert result.inserted_id is not None
        return document
    
    def matching(self, query: Search) -> List[T]:
        q = query.construct_query()
        results = self.find_by(q)
        # TODO: Hack...
        t = query.get_id_term()
        if t is not None:
            results = filter(
                lambda res: t in str(res.id),
                results
            )
        return list(results)
    
    def exists(self, id: str) -> bool:
        document = self.find_one_by_id(id)
        return bool(document)
    
    def assert_exists(self, id: str) -> None:
        self.get(id)
    
    def get(self, id: str) -> T:
        print("About to look for", id)
        document = self.find_one_by_id(id)
        if not document:
            raise NotFoundException(f"Unable to find {self.desc} {id}")
        return document

    # def _create_inner(self, data: Optional[Dict] = None) -> str:
    #     uuid = create_uuid()
    #     while self.exists(uuid):
    #         uuid = create_uuid()
    #         # raise AlreadyExistsException(f"This {self.desc} already exists")
    #     current_time = get_time()
    #     document = dict(
    #         created=current_time,
    #         updated=current_time,
    #         _id=uuid,
    #     )
    #     if data is not None:
    #         document.update(data)
    #     result = self.collection.insert_one(document)
    #     assert result.acknowledged
    #     return result.inserted_id
    
    # def create(self, data: Optional[Dict] = None) -> T:
    #     inserted_id = self._create_inner(data)
    #     return self.get(inserted_id)

    # def update(self, id: str, updates: JsonUpdates):
    #     document = updates.dict()
        
    #     # TODO: Make this be actual edits, not overrides
    #     document["updated"] = get_time()
        
    #     # TODO:
    #     # use a json diffing tool
    #     # or, use a Ast for mongo set...
        
    #     result = self.collection.update_one({"_id": id}, {"$set": document})
    #     if not result.modified_count:
    #         raise NotFoundException(f"Unable to find {self.desc} {id}")

    # This overrides the super's
    def my_delete(self, id: str):
        result = self.get_collection().delete_one({"_id": ObjectId(id)})
        if not result.deleted_count:
            raise NotFoundException(f"Unable to delete {self.desc} {id}")
