from common.model.project import Project

from serve.database import db

from serve.repositories.base import BaseRepository
from serve.cfg import mongo_settings

from typing import Any, Dict


class ProjectRepository(BaseRepository[Project]):
    desc: str
    
    class Meta:
        collection_name = mongo_settings.project_collection


repository: ProjectRepository = ProjectRepository(
    database=db,
    # collection=db.project_collection,
    desc="project",
)
