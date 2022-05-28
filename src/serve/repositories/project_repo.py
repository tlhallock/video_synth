from typing import Dict
from bson import List
from common.model.project import Project

import serve.database as db

from serve.repositories.base_repo import BaseRepository


def project_constructor(json: Dict) -> Project:
    id = json["_id"]
    del json["_id"]
    return Project(**json, id=id)


repository: BaseRepository[Project] = BaseRepository(
    constructor=project_constructor,
    collection=db.project_collection,
    desc="project",
)
