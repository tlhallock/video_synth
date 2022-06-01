
from typing import Any, Dict, List

import click
from pydantic import BaseModel

class Option(BaseModel):
    args: List[str]
    kwargs: Dict[str, Any]


list_output = Option(
    args=["-o", "--output", "format"],
    kwargs=dict(
        # default="rich",
        type=click.Choice(["rich", "yaml", "json", "csv"], case_sensitive=False),
        help="Output format"))