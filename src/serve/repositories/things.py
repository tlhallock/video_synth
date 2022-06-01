
from common.model.thing import Thing

import serve.database as db
from serve.repositories.base import BaseRepository


from serve.database import db

from serve.repositories.base import BaseRepository
from serve.cfg import mongo_settings


# These should be deleted when the project is deleted...

class ThingRepository(BaseRepository[Thing]):
    desc: str
    
    class Meta:
        collection_name = mongo_settings.thing_collection


repository: ThingRepository = ThingRepository(
    database=db,
    desc="thing",
)
