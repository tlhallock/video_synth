from typing import List, Optional
from contextlib import suppress
import dateutil
import datetime
import pydantic
from pydantic import Field

from .base import BaseModel
from .fields import Details
from .person_address import Address

__all__ = ("ProjectUpdates", "Project", "Projects", "CreateProjectArgs")


class AddScene(BaseModel):
    project_id: str = Field(**Details.identifer)
    name: Optional[str]
    num_frames: int


class Scene(BaseModel):
    id: str = Field(**Details.identifer)
    project_id: str = Field(**Details.identifer)

    @pydantic.root_validator(pre=True)
    @classmethod
    def _set_id(cls, data):
        document_id = data.get("_id")
        if document_id:
            data["id"] = document_id
        return data
