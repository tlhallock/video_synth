

from typing import Callable, Dict, Generic, List, Optional, TypeVar

import pymongo

from common.model.base import BaseModel
from common.utils import get_time, create_uuid
from serve.exceptions import NotFoundException
from common.schema.updates import JsonUpdates


T = TypeVar('T')

class BaseRepository(Generic[T]): # BaseModel
    collection: pymongo.collection
    constructor: Callable[[Dict], T]
    desc: str
    
    # TODO: Remove this:
    def __init__(
        self,
        collection: pymongo.collection,
        constructor: Callable[[Dict], T],
        desc: str
    ) -> None:
        super().__init__()
        self.collection = collection
        self.constructor = constructor
        self.desc = desc
    
    def list(self, filter: Optional[Dict] = None) -> List[T]:
        if filter is None:
            cursor = self.collection.find()
        else:
            cursor = self.collection.find(filter)
        return [self.constructor(document) for document in cursor]
    
    def exists(self, id: str) -> bool:
        document = self.collection.find_one({"_id": id})
        return bool(document)
    
    def assert_exists(self, id: str) -> None:
        if not self.exists(id):
            raise NotFoundException(f"Unable to find {self.desc} {id}")
    
    def get(self, id: str) -> T:
        document = self.collection.find_one({"_id": id})
        if not document:
            raise NotFoundException(f"Unable to find {self.desc} {id}")
        return self.constructor(document)

    def create(self, data: Optional[Dict] = None) -> T:
        uuid = create_uuid()
        while self.exists(uuid):
            uuid = create_uuid()
            # raise AlreadyExistsException(f"This {self.desc} already exists")
        current_time = get_time()
        document = dict(
            created=current_time,
            updated=current_time,
            _id=uuid,
        )
        if data is not None:
            document.update(data)
        result = self.collection.insert_one(document)
        assert result.acknowledged
        return self.get(result.inserted_id)

    def update(self, id: str, updates: JsonUpdates):
        document = updates.dict()
        
        # TODO: Make this be actual edits, not overrides
        document["updated"] = get_time()
        
        # TODO:
        # use a json diffing tool
        # or, use a Ast for mongo set...
        
        result = self.collection.update_one({"_id": id}, {"$set": document})
        if not result.modified_count:
            raise NotFoundException(f"Unable to find {self.desc} {id}")

    def delete(self, id: str):
        result = self.collection.delete_one({"_id": id})
        if not result.deleted_count:
            raise NotFoundException(f"Unable to delete {self.desc} {id}")
    
    class Config:
        arbitrary_types_allowed = True
