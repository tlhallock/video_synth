
import click
import json

from datetime import datetime

# def find_project(client: Client, id: str):

def my_default(o):
    if isinstance(o, datetime):
        return str(o)
    return json.JSONEncoder.default(o)