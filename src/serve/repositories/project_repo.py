from typing import Dict
from bson import List
from common.schema.project import (
    CreateProjectArgs,
    ProjectUpdates,
    Project,
)
from ..exceptions import (
    NotFoundException,
)

import serve.database as db


from serve.repositories.base_repo import BaseRepository


def project_constructor(json: Dict) -> Project:
    return Project(**json, **json["data"])


repository: BaseRepository[Project] = BaseRepository(
    constructor=project_constructor,
    collection=db.project_collection,
    desc="project",
)


# class ProjectRepository:
#     @staticmethod
#     def get(id: str) -> Project:
#         document = db.project_collection.find_one({"_id": id})
#         if not document:
#             raise NotFoundException("Unable to find project f{id}")
#         return Project(**document)

#     @staticmethod
#     def list() -> List[Project]:
#         cursor = db.project_collection.find()
#         return [Project(**document) for document in cursor]

#     @staticmethod
#     def create(args: CreateProjectArgs) -> Project:
#         document = args.dict()
#         document["created"] = document["updated"] = get_time()
#         document["_id"] = create_uuid()
#         # The time and id could be inserted as a model's Field default factory,
#         # but would require having another model for Repository only to implement it

#         print('document', document)
#         result = db.project_collection.insert_one(document)
#         assert result.acknowledged

#         print('result', result)
#         return ProjectRepository.get(result.inserted_id)

#     @staticmethod
#     def update(id: str, updates: ProjectUpdates):
#         document = updates.dict()
        
#         # TODO: Make this be actual edits, not overrides
#         document["updated"] = get_time()

#         result = db.project_collection.update_one({"_id": id}, {"$set": document})
#         if not result.modified_count:
#             raise NotFoundException(f"Unable to find project {id}")

#     @staticmethod
#     def delete(id: str):
#         result = db.project_collection.delete_one({"_id": id})
#         if not result.deleted_count:
#             raise NotFoundException(identifier=id)