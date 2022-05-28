
from typing import List
from numpy import str0
import strawberry
from src.common.schema.thing import AddThingArgs
from src.serve.repositories.thing_repo import ThingRepository


from src.serve.repositories.project_repo import ProjectRepository


from .mapping import (
    CreateProjectInput,
    ProjectType,
    AddThingInput,
    ThingType,
)


@strawberry.type
class Query:
    @strawberry.field
    def projects(self) -> List[ProjectType]:
        return ProjectRepository.list()
    
    @strawberry.field
    def project(self, id: str) -> ProjectType:
        return ProjectRepository.get(id)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_project(self, name: str) -> ProjectType:
        return ProjectRepository.create(name=name)
    
    @strawberry.mutation
    def add_thing(self, project: str, thing: AddThingInput) -> ThingType:
        return ThingRepository.add(project, thing.to_pydantic())


projects_schema = strawberry.Schema(Query, Mutation)
