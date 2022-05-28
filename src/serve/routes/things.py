from typing import List
from fastapi import APIRouter, Depends
from fastapi import status as statuscode

from common.model.thing import (
    AddThingArgs,
    Thing,
    ThingUpdates,
)

from serve.exceptions import (
    get_exception_responses,
    NotFoundException,
    AlreadyExistsException,
)

from serve.schemas.project import router as project_router
from serve.repositories.project_repo import repository as project_repo


from serve.repositories.thing_repo import repository


@project_router.get(
    "/{project}/things",
    response_model=List[Thing],
    description="List the things in a project",
)
def _list(project):
    project_repo.assert_exists(project)
    return repository.list({project: project})


@project_router.post(
    "/{project}/things",
    description="Add a new thing to a project",
    response_model=Thing,
    status_code=statuscode.HTTP_201_CREATED,
    responses=get_exception_responses(AlreadyExistsException),
)
def _create(project: str, args: AddThingArgs):
    return repository.create(data=dict(**args.dict(), project=project))



router = APIRouter(
    prefix="/things",
    tags=["things"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/{id}",
    response_model=Thing,
    description="Get a single thing by its unique ID",
    responses=get_exception_responses(NotFoundException),
)
def _get(id: str):
    return repository.get(id)



@router.patch(
    "/{id}",
    description="Update a single thing by its unique ID, providing the fields to update",
    status_code=statuscode.HTTP_204_NO_CONTENT,
    responses=get_exception_responses(NotFoundException, AlreadyExistsException),
)
def _update(id: str, update: ThingUpdates):
    repository.update(id, update)


@router.delete(
    "/{id}",
    description="Delete a single thing by its unique ID",
    status_code=statuscode.HTTP_204_NO_CONTENT,
    responses=get_exception_responses(NotFoundException),
)
def _delete(id: str):
    repository.delete(id)

