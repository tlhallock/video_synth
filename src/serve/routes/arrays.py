from typing import List, Optional
from fastapi import APIRouter
from fastapi import status as statuscode
import json

from common.model.array_info import (
    CreateArrayInfo,
    ArrayInfo,
)

from serve.exceptions import (
    get_exception_responses,
    NotFoundException,
    AlreadyExistsException,
)

from common.model.file_info import SynchonizeResult

from serve.routes.projects import router as project_router
from serve.repositories.projects import repository as project_repo

from serve.routes.things import router as thing_router
from serve.repositories.things import repository as thing_repo

from serve.repositories.arrays import repository


@project_router.get(
    "/{project}/arrays",
    response_model=List[ArrayInfo],
    description="List the arrays in a project",
)
def _list_under_project(project):
    project_repo.assert_exists(project)
    return repository.list(dict(project=project))


@thing_router.get(
    "/{thing}/arrays",
    response_model=List[ArrayInfo],
    description="List the arrays in a thing",
)
def _list_under_thing(thing):
    thing_repo.assert_exists(thing)
    return repository.list(dict(thing=thing))


router = APIRouter(
    prefix="/arrays",
    tags=["arrays"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/",
    response_model=List[ArrayInfo],
    description="List all the arrays",
)
def _list():
    return repository.list()


@router.get(
    "/search",
    response_model=List[ArrayInfo],
    description="Search for a array with a regular expression on the id.",
)
def _search(id: str):
    return repository.matching(dict(_id={"$regex": id}))


@router.get(
    "/{id}",
    response_model=ArrayInfo,
    description="Get a single array by its unique ID",
    responses=get_exception_responses(NotFoundException),
)
def _get(id: str):
    return repository.get(id)


@router.post(
    "/",
    description="Add a new array to a project or thing",
    response_model=ArrayInfo,
    status_code=statuscode.HTTP_201_CREATED,
    responses=get_exception_responses(AlreadyExistsException),
)
def _create(args: CreateArrayInfo):
    js = json.loads(args.json())
    js["revision"] = 0
    return repository.create(data=js)


@router.patch(
    "/{id}",
    description="Synchronize a single array by its unique ID, providing the fields to update",
    response_model=SynchonizeResult,
    responses=get_exception_responses(NotFoundException, AlreadyExistsException),
)
def _update(id: str) -> SynchonizeResult:
    repository.synchronize_entry(id)
    
    

@router.patch(
    "/",
    description="Synchronize the arrays collection with the contents on disk",
    response_model=SynchonizeResult,
)
def _sync() -> SynchonizeResult:
    repository.synchronize()


@router.delete(
    "/{id}",
    description="Delete a single thing by its unique ID",
    status_code=statuscode.HTTP_204_NO_CONTENT,
    responses=get_exception_responses(NotFoundException),
)
def _delete(id: str):
    repository.delete(id)

