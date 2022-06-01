
import click

from common.model.project import Project
from cli.client.projects import ProjectsClient as Client
from cli.formats.formats import show_list, show_single
from cli.options import list_output
from cli.aliased_group import AliasedGroup

@click.group(cls=AliasedGroup)
@click.pass_context
def projects(ctx):
    pass

cmd = projects
clazz = Project


@cmd.command()
@click.option(*list_output.args, **list_output.kwargs, default="rich")
def list(format):
    """List projects
    """
    client = Client.create_client()
    entries = client.list()
    show_list(
        clazz=clazz,
        entries=entries,
        title="projects",
        format=format,
    )


@cmd.command()
@click.argument("id")
@click.option(*list_output.args, **list_output.kwargs, default="yaml")
def get(id: str, format: str):
    """Search for a project containing string id in its id
    """
    client = Client.create_client()
    entry = client.find(id=id)
    show_single(clazz=clazz, entry=entry, format=format)


@cmd.command()
@click.argument("id")
def visit(id: str):
    """Get a project's url
    """
    client = Client.create_client()
    entry = client.find(id=id)
    url = f"http://localhost:3000/project/{entry.id}"
    click.echo(f"Visiting {url}")
    click.launch(url)


@cmd.command()
@click.argument("name")
@click.option(*list_output.args, **list_output.kwargs, default="yaml")
def create(name: str, format: str):
    """Create a project with the given name
    """
    client = Client.create_client()
    entry = client.create_project(name=name)
    show_single(clazz=clazz, entry=entry, format=format)


@cmd.command()
@click.argument("id")
def delete(id: str):
    """Delete a project given a substring of its identifier
    """
    client = Client.create_client()
    entry = client.find(id=id)
    resp = client.delete(id=entry.id)
    if not resp:
        raise click.ClickException(f"Unable to delete entry {entry.id}")
    click.echo(f"Successfully deleted {entry.id}")

