
import click

from cli.aliased_group import AliasedGroup

from cli.cmds.projects import projects
from cli.cmds.things import things
from cli.cmds.videos import videos
# from cli.arrays import arrays


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS, cls=AliasedGroup)
def cli():
    pass


cli.add_command(projects)
cli.add_command(things)
cli.add_command(videos)
# cli.add_command(arrays)

