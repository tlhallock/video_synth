


from datetime import datetime
from typing import Optional
from bson import ObjectId
from pydantic import Field, validator
from pydantic_mongo import ObjectIdField

from common.model.base import Fields
from common.utils.utils import get_time

from common.model.base import BaseModel


class Storable(BaseModel):
    # TODO: Shouldn't need pydantic_mongo on the client...
    # TODO: Shouldn't expose the mongo id field
    # TODO: Should have an uuid field 
    id: ObjectIdField = None
    created: datetime = Field(**Fields.unix_ts, default_factory=get_time)
    updated: datetime = Field(**Fields.unix_ts, default_factory=get_time)
    
    def as_updates(self, other: "Storable") -> None:
        self.id = other.id
        self.created = other.created
        self.updated = get_time()

    class Config:
        # The ObjectIdField creates an bson ObjectId value, so its necessary to setup the json encoding
        json_encoders = {ObjectId: str}
        
