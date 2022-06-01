
from sys import implementation
from typing import Optional
import click
import yaml

from common.model.array_info import ArrayInfo, CreateArrayInfo
from cli.client.arrays import ArraysClient as Client
from cli.client.projects import ProjectsClient
from cli.client.things import ThingsClient
from cli.formats.formats import show_list, show_single
from cli.options import list_output
from cli.aliased_group import AliasedGroup


@click.group(cls=AliasedGroup)
@click.pass_context
def arrays(ctx):
    pass

cmd = arrays
clazz = ArrayInfo


@cmd.command()
@click.option(*list_output.args, **list_output.kwargs, default="rich")
@click.option("-p", "--project", "project", default=None, type=str, help="A project to limit results")
@click.option("-t", "--thing", "thing", default=None, type=str, help="A thing to limit results")
def list(format: str, project: str, thing: str):
    """List things under a project
    """
    client = Client.create_client()
    if project is None and thing is None:
        entries = client.list()
    elif thing is not None:
        thing_client = ThingsClient.create_client()
        thing_id = thing_client.find(thing).id
        click.echo(f"Listing arrays under thing {thing_id}")
        entries = client.list_under_thing(thing_id)
    elif project is not None:
        project_client = ProjectsClient.create_client()
        project_id = project_client.find(project).id
        click.echo(f"Listing array under project {project_id}")
        entries = client.list_under_project(project_id)
    show_list(
        clazz=clazz,
        entries=entries,
        title="arrays",
        format=format,
    )


# def get_project(kwargs):
#     project_client = ProjectsClient.create_client()
#     project_id = project_client.find(kwargs["project"]).id
#     return project_id
    

# def create_initial_args(kwargs):
#     has_project = "project" in kwargs and kwargs["project"] is not None
    
#     if "file" in kwargs and kwargs["file"] is not None:
#         with open(kwargs["file"], "r") as infile:
#             y = yaml.full_load(infile)
#             if has_project:
#                 y["project"] = get_project(kwargs)
#             return AddThingArgs(**y)
        
#     if not has_project:
#         raise click.ClickException("Not reading from file, and no project given.")
    
#     if "thing_type" not in kwargs or kwargs["thing_type"] is None:
#         raise click.ClickException("Not reading from file, and no type given.")
        
#     return AddThingArgs(
#         project=get_project(kwargs),
#         type=ThingType(kwargs["thing_type"]),
#         implementation=kwargs["implementation"],
#         implmentation_version=kwargs["impl_version"],
#         name=kwargs["name"],
#         data=None,
#     )


# def edit_args(args: AddThingArgs):
#     current_text = yaml.dump(args.dict())
#     updated_text = click.edit(current_text)
#     if updated_text is None:
#         updated_text = current_text
#     try:
#         y = yaml.load(updated_text, Loader=yaml.Loader)
#         return AddThingArgs(**y)
#     except Exception as e:
#         with open("invalid.yaml", "w") as outfile:
#             outfile.write(updated_text)
#         s = "Unable to parse updated text"
#         print(s)
#         raise e
#         # raise click.ClickException(s)


# @cmd.command()
# @click.option(
#     "-t", "--type", "thing_type", 
#     default=None, 
#     type=click.Choice(
#         [ttype.name for ttype in ThingType], case_sensitive=True),
#     help="The type of the thing being created.")
# @click.option(
#     "-i", "--implementation", "impl", 
#     default=None,
#     type=str,
#     help="The implementation of this thing.")
# @click.option(
#     "-n", "--name", "name", 
#     default=None,
#     type=str,
#     help="An optional name for this thing.")
# @click.option(
#     "-v", "--impl-version", "impl_version", 
#     default=None, 
#     type=str,
#     help="The version of the implementation of this thing.")
# @click.option(
#     "-f", "--file", "file", 
#     default=None, 
#     type=str,
#     # type=click.File("r"),
#     help="Create the thing from the given file.")
# @click.option(
#     "-e", "--edit", "edit", 
#     default=True, type=bool, help="Edit the thing before creating.")
# @click.option(
#     "-p", "--project", "project", 
#     default=None, type=str, help="The project to place this thing in.")
# @click.option(*list_output.args, **list_output.kwargs, default="yaml")
# def create(**kwargs):
#     """Create a thing with edited parameters
#     """
#     args = create_initial_args(kwargs)
#     if "edit" in kwargs and kwargs["edit"]:
#         args = edit_args(args)
        
#     client = Client.create_client()
#     entry = client.create_thing(args=args)
#     show_single(clazz=clazz, entry=entry, format=kwargs["format"])
    


@cmd.command()
@click.argument("id")
@click.option(*list_output.args, **list_output.kwargs, default="yaml")
def get(id: str, format: str):
    """Search for an array containing string id in its id
    """
    client = Client.create_client()
    entry = client.find(id)
    show_single(clazz=clazz, entry=entry, format=format)


@cmd.command()
@click.argument("id")
def visit(id: str):
    """Get an array's url
    """
    client = Client.create_client()
    entry = client.find(id)
    url = f"http://localhost:3000/array/{entry.id}"
    click.echo(f"Visiting {url}")
    click.launch(url)


@cmd.command()
@click.argument("id")
def delete(id: str):
    """Delete an array given a substring of its identifier
    """
    client = Client.create_client()
    entry = client.find(id=id)
    resp = client.delete(id=entry.id)
    if not resp:
        raise click.ClickException(f"Unable to delete entry {entry.id}")
    click.echo(f"Successfully deleted {entry.id}")
