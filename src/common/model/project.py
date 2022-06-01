from datetime import datetime
from typing import Any, Dict, List, Optional
import pydantic
from pydantic import Field

from common.utils import create_uuid, get_time

from common.model.base import BaseModel
from common.model.base import Fields
from common.model.storable import Storable




class ProjectUpdates(BaseModel):
    name: Optional[str] = None
    
    def creation_data(self) -> Dict[str, Any]:
        return self.dict()


class Project(Storable):
    name: str


class CreateProjectArgs(BaseModel):
    name: str
    
    def create(self) -> Project:
        return Project(**self.dict())

    # @pydantic.root_validator(pre=True)
    # @classmethod
    # def _set_id(cls, data):
    #     document_id = data.get("_id")
    #     if document_id:
    #         data["id"] = document_id
    #     return data

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
