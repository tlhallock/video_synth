
from sys import implementation
from typing import Optional
import click
import yaml

from client.videos import VideosClient as Client
from client.projects import ProjectsClient
from client.things import ThingsClient
from cli.formats.formats import show_list, show_single
from cli.options import list_output
from cli.aliased_group import AliasedGroup
from common.model.fs_resource import SynchonizeResult
from common.model.video_info import VideoInfo

@click.group(cls=AliasedGroup)
@click.pass_context
def videos(ctx):
    pass

cmd = videos
clazz = VideoInfo


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
        click.echo(f"Listing videos under thing {thing_id}")
        entries = client.list_under_thing(thing_id)
    elif project is not None:
        project_client = ProjectsClient.create_client()
        project_id = project_client.find(project).id
        click.echo(f"Listing videos under project {project_id}")
        entries = client.list_under_project(project_id)
    show_list(
        clazz=clazz,
        entries=entries,
        title="videos",
        format=format,
    )


@cmd.command()
@click.option("-i", "--id", "id", type=str, default=None, help="The identifier of the video")
@click.option("-c", "--checksum", "checksum", type=str, default=None, help="The checksum of the video")
@click.option(*list_output.args, **list_output.kwargs, default="yaml")
def get(id: str, checksum: str, format: str):
    """Search for a video containing string id in its id
    """
    client = Client.create_client()
    entry = client.find(id=id, checksum=checksum)
    show_single(clazz=clazz, entry=entry, format=format)


@cmd.command()
@click.argument("id")
def visit(id: str):
    """Get an array's url
    """
    client = Client.create_client()
    entry = client.find(id=id)
    url = f"http://localhost:3000/video/{entry.info.checksum}"
    click.echo(f"Visiting {url}")
    click.launch(url)


@cmd.command()
@click.option("-i", "--id", "id", type=str, default=None, help="The identifier of the video")
@click.option(*list_output.args, **list_output.kwargs, default="yaml")
def synchronize(id: Optional[str], format: str):
    """Synchronize the collection with contents on disk.
    """
    client = Client.create_client()
    if id is None:
        resp = client.synchronize()
    else:
        resp = client.synchronize(id=id)
    if not resp:
        raise click.ClickException(f"Unable to synchronize video {id}")
    show_single(clazz=SynchonizeResult, entry=resp, format=format)
    click.echo(f"Successfully synchronized video {id}")

