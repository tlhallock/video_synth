
from common.model.thing import Thing

import serve.database as db
from serve.repositories.base_repo import BaseRepository


# These should be deleted when the project is deleted...


def create_thing(json: dict) -> Thing:
    return Thing(**json, **json["data"])


repository: BaseRepository[Thing] = BaseRepository(
    collection=db.thing_collection,
    constructor=create_thing,
    desc="thing"
)