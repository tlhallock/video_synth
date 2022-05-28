from typing import Dict
from bson import List
from common.model.project import Project

import serve.database as db

from serve.repositories.base_repo import BaseRepository


def project_constructor(json: Dict) -> Project:
    return Project(**json)


repository: BaseRepository[Project] = BaseRepository(
    constructor=project_constructor,
    collection=db.project_collection,
    desc="project",
)
