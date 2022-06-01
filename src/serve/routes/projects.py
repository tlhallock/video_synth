from typing import List, Optional
from fastapi import APIRouter
from fastapi import status as statuscode

from common.model.project import (
    CreateProjectArgs,
    Project,
    ProjectUpdates,
)

from serve.exceptions import (
    get_exception_responses,
    NotFoundException,
    AlreadyExistsException,
)
from serve.repositories.projects import repository
from common.model.search import Search



router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/",
    response_model=List[Project],
    description="List all the available projects",
)
def _list():
    return repository.list()


@router.get(
    "/search",
    response_model=List[Project],
    description="Search for a project with a regular expression",
)
def _search(query: Search):
    return repository.matching(query)


@router.get(
    "/{id}",
    response_model=Project,
    description="Get a single project by its unique ID",
    responses=get_exception_responses(NotFoundException),
)
def _get(id: str):
    return repository.get(id)


@router.post(
    "/",
    description="Create a new project",
    response_model=Project,
    status_code=statuscode.HTTP_201_CREATED,
    responses=get_exception_responses(AlreadyExistsException),
)
def _create(args: CreateProjectArgs):
    # TODO: create unique name constraint
    # TODO: Already exists exception
    project = args.create()
    return repository.create(project)


@router.patch(
    "/{id}",
    description="Update a single project by its unique ID, providing the fields to update",
    status_code=statuscode.HTTP_204_NO_CONTENT,
    responses=get_exception_responses(NotFoundException, AlreadyExistsException),
)
def _update(id: str, update: ProjectUpdates):
    repository.update(id, update)


@router.delete(
    "/{id}",
    description="Delete a single project by its unique ID",
    status_code=statuscode.HTTP_204_NO_CONTENT,
    responses=get_exception_responses(NotFoundException),
)
def _delete(id: str):
    repository.my_delete(id)
