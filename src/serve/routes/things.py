from typing import List, Optional
from fastapi import APIRouter
from fastapi import status as statuscode
import json

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

from serve.routes.projects import router as project_router
from serve.repositories.projects import repository as project_repo

from serve.repositories.things import repository
from src.common.model.search import Search


@project_router.get(
    "/{project}/things",
    response_model=List[Thing],
    description="List the things in a project",
)
def _list_under(project):
    project_repo.assert_exists(project)
    return repository.list(dict(project=project))


router = APIRouter(
    prefix="/things",
    tags=["things"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/",
    response_model=List[Thing],
    description="List all the things",
)
def _list():
    return repository.list()


@router.get(
    "/search",
    response_model=List[Thing],
    description="Search for a thing with a regular expression on the id.",
)
def _search(query: Search):
    return repository.matching(query)


@router.get(
    "/{id}",
    response_model=Thing,
    description="Get a single thing by its unique ID",
    responses=get_exception_responses(NotFoundException),
)
def _get(id: str):
    return repository.get(id)


@router.post(
    "/",
    description="Add a new thing to a project",
    response_model=Thing,
    status_code=statuscode.HTTP_201_CREATED,
    responses=get_exception_responses(AlreadyExistsException),
)
def _create(args: AddThingArgs):
    thing = args.create()
    return repository.create(document=thing)


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
    repository.my_delete(id)

