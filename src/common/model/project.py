from typing import List, Optional
import pydantic
from pydantic import Field

from common.utils import create_uuid, get_time

from common.model.base import BaseModel
from common.model.base import Fields


class CreateProjectArgs(BaseModel):
    name: str


class ProjectUpdates(BaseModel):
    name: Optional[str] = None

    def dict(self, **kwargs):
        d = super().dict(**kwargs)
        # with suppress(KeyError):
        #     d["birth"] = d.pop("birth").isoformat()
        return d


class Project(BaseModel):
    id: str = Field(**Fields.identifer, default_factory=create_uuid)
    name: str
    created: int = Field(**Fields.unix_ts, default_factory=get_time)
    updated: int = Field(**Fields.unix_ts, default_factory=get_time)

    @pydantic.root_validator(pre=True)
    @classmethod
    def _set_id(cls, data):
        document_id = data.get("_id")
        if document_id:
            data["id"] = document_id
        return data

    # @pydantic.root_validator()
    # @classmethod
    # def _set_age(cls, data):
    #     birth = data.get("birth")
    #     if birth:
    #         today = datetime.datetime.now().date()
    #         data["age"] = dateutil.relativedelta.relativedelta(today, birth).years
    #     return data

    class Config(BaseModel.Config):
        extra = pydantic.Extra.ignore  # if a read document has extra fields, ignore them
