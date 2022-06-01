
import click

from common.model.project import Project
from cli.client.projects import ProjectsClient as Client
from cli.formats.formats import show_list, show_single
from cli.options import list_output
from cli.aliased_group import AliasedGroup

@click.group(cls=AliasedGroup)
@click.pass_context
def calc(ctx):
    pass

cmd = calc


@cmd.command()
@click.argument("filename")
def delete(filename: str):
    """Delete a thing given a substring of its identifier
    """
    client = Client.create_client()
    entry = client.find(id=id)
    resp = client.delete(id=entry.id)
    if not resp:
        raise click.ClickException(f"Unable to delete entry {entry.id}")
    click.echo(f"Successfully deleted {entry.id}")


