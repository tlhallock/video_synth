
from typing import Any, List, Optional, Type

import click
from cli.formats.yaml_response import YamlListResponse, YamlSingleResponse
from cli.formats.rich_format import RichListResponse
from pydantic import BaseModel

from cli.formats.base import ListResponse, SingleResponse
from cli.formats.json_response import JsonListResponse, JsonSingleResponse
from cli.formats.csv_response import CsvListResponse


# TODO: Push this parsing into the actual command line arguments

def create_list_response(
    clazz: Type[BaseModel],
    format: str,
    title: Optional[str] = None,
) -> ListResponse:
    if format == "yaml":
        return YamlListResponse.create(
            title=title
        )
    if format == "json":
        return JsonListResponse.create(
            title=title,
        )
    if format == "rich":
        return RichListResponse.create(
            clazz=clazz,
            title=title,
        )
    if format == "csv":
        return CsvListResponse.create(
            clazz=clazz,
            title=title,
        )
    raise click.ClickException("No output format!")


def create_single_response(clazz: Type[BaseModel], entry: BaseModel, format: str) -> SingleResponse:
    if format == "json":
        return JsonSingleResponse.create(entry)
    if format == "yaml":
        return YamlSingleResponse.create(entry)
    
    resp = create_list_response(clazz=clazz, format=format, title="result")
    resp.add(entry)
    return resp


def show_list(
    clazz: Type[BaseModel],  # Should be able to delete this parameter with a generic?
    entries: List[BaseModel],
    format: str,
    title: Optional[str] = None,
) -> None:
    response = create_list_response(clazz=clazz, title=title, format=format)
    response.show(entries)


def show_single(
    clazz: Type[BaseModel],
    entry: BaseModel,
    format: str,
) -> None:
    response = create_single_response(clazz=clazz, entry=entry, format=format)
    response.print()
