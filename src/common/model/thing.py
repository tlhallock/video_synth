from optparse import Option
from pydantic import Field, Json
from typing import List, Optional, Sequence
from contextlib import suppress
import dateutil
import datetime
import pydantic
from enum import Enum, auto
from typing import List, Optional
import numpy as np
import math

from common.utils import create_uuid, get_time, get_uuid

from .base import BaseModel
from .fields import Details


class ThingType(Enum):
    STREAM = auto
        # can be original(source), rendered, or intermediate, debug
        # has a map to active frames
        # could be used as a background
        # has a path on disk
        # can have a layer, if it is intermediate
    CAMERA = auto
        # has a map to active frames
        # has an intrinsics
        # has a pose per frame
        # can be approximate a real camera?, or be a pinhole camera
    MODEL = auto
        # has a map to active frames
        # may have textures
        # may have global parameters
        # has a layer
    LIGHT = auto
        # has a map to active frames
        # has an intensity
        # maybe pose
        # maybe it has a color
    CALC = auto
        # has a map to active frames
        # has an array
        # has a name
        # represents a namespace for 


# TODO: wrote this thinking it was a thing
class AddThingArgs(BaseModel):
    id: str = Field(**Details.identifer)
    project: str = Field(**Details.identifer)
    created: int = Field(**Details.unix_ts) #, default_factory=get_time)
    updated: int = Field(**Details.unix_ts) #, default_factory=get_time)
    
    type: ThingType
    implementation: str
    implmentation_version: str
    revision: int
    
    name: Optional[str]
    data: str
    # params: Json
    

class Thing(BaseModel):
    id: str = Field(**Details.identifer)
    project_id: str = Field(**Details.identifer)
    
    category: str
    type: str
    model_version: str
    name: Optional[str]
    params: str
    # params: Json  # Could be a union of currently supported types

    @pydantic.root_validator(pre=True)
    @classmethod
    def _set_id(cls, data):
        document_id = data.get("_id")
        if document_id:
            data["id"] = document_id
        return data


class ThingUpdates(BaseModel):
    id: str = Field(**Details.identifer)
    
    category: Optional[str]
    type: Optional[str]
    model_version: Optional[str]
    name: Optional[str]
    param_updates: str
    # param_updates: Json  # Make a specific type


# class Placement(BaseModel):
#     # Dimensions: frame x 3(x/y/z)
#     world_translation: np.ndarray
#     # Dimensions: frame x 4(quaternion)
#     world_rotation: np.ndarray
#     # Scaling
    
#     # Dimension: frame x # pose params
#     pose: Optional[np.ndarray]



# class Place(BaseModel):
#     thing_id = Field(
#         description="Unique identifier of this thing",
#         example=get_uuid(),
#         min_length=36,
#         max_length=36
#     )
    