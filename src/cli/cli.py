
import click

from cli.aliased_group import AliasedGroup

from cli.cmds.projects import projects
from cli.cmds.things import things
from cli.cmds.videos import videos
from cli.cmds.arrays import arrays
from cli.cmds.calc import calc


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS, cls=AliasedGroup)
def cli():
    pass


cli.add_command(projects)
cli.add_command(things)
cli.add_command(videos)
cli.add_command(arrays)
cli.add_command(calc)

