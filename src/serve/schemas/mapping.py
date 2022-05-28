
from typing import List
import strawberry

from common.schema.project import (
    CreateProjectArgs,
    Project,
    ProjectUpdates,
)

from common.schema.thing import (
    AddThingArgs,
    Thing,
    ThingUpdates,
)


from src.serve.repositories.project_repo import ProjectRepository


@strawberry.experimental.pydantic.input(model=CreateProjectArgs, all_fields=True)
class CreateProjectInput:
    pass

@strawberry.experimental.pydantic.type(model=Project, all_fields=True)
class ProjectType:
    pass


@strawberry.experimental.pydantic.input(model=AddThingArgs, all_fields=True)
class AddThingInput:
    pass


@strawberry.experimental.pydantic.type(model=Thing, all_fields=True)
class ThingType:
    pass
