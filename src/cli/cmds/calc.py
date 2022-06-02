
import typing

import click
from cli.aliased_group import AliasedGroup
from cli.formats.formats import show_list, show_single
from cli.options import list_output
from client.things import ThingsClient
from client.videos import VideosClient
from common.model.thing import StreamData, ThingType


@click.group(cls=AliasedGroup)
@click.pass_context
def calc(ctx):
    pass

cmd = calc


@cmd.command()
@click.argument("video")
def tomasi(video: str):
    """Run feature tracking with shi tomasi corner detection
    
    VIDEO: the id of the thing for the video
    """
    things_client = ThingsClient.create_client()
    video_info = things_client.find(id=video)
    assert video_info.type == ThingType.STREAM
    data = typing.cast(StreamData, video_info.data)
    
    videos_client = VideosClient.create_client()
    video_info = videos_client.get(data.video_id)
    
    print(video_info.info)


