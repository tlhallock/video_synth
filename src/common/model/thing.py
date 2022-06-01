from pydantic import Field, Json
from typing import Any, Dict, Optional, Sequence, Tuple, Union
import datetime
import pydantic
from enum import Enum, auto
from typing import List, Optional
from datetime import datetime

from common.model.base import BaseModel, Fields
from common.model.frame_map import FrameMap
from pydantic_mongo import ObjectIdField

from common.model.storable import Storable


class StreamType(Enum):
    ORIGINAL = "source"
    INTERMEDIATE = "intermediate"
    RENDERED = "rendered"
    DEBUG = "debug"
    

class StreamData(BaseModel):
    video_id: str
    stream_type: StreamType
    frame_map: FrameMap
    # -1 for source, 0 for background, 1... for models?
    layer: int
    


class CameraData(BaseModel):
    # source camera?
    intrinsics: str = "not implemented"
    
    # pinhole camera
    resolution: Sequence[int]
    physical_dims: Tuple[float, float]
    focal_length: float
    
    poses: Optional[str] = None
    pose_map: FrameMap
    
    
class ModelData(BaseModel):
    # Assumed to be the STAR human model for now...
    texture: Optional[str] = None
    betas: Optional[str] = None
    poses: Optional[str] = None
    pose_map: FrameMap
    layer: Optional[int] = None
    

class LightData(BaseModel):
    intensity: float = 1
    color: Tuple[float, float, float] = Field(default_factory=lambda:tuple(1.0, 1.0, 1.0))
    
    pose: Optional[str] = None
    pose_map: FrameMap


class CalculationData(BaseModel):
    calculation_name: str
    # More info...
    array: str
    map: FrameMap
    


class ThingType(Enum):
    STREAM = "video"
    CAMERA = "camera"
    MODEL = "model"
    LIGHT = "light"
    CALC = "calculation"
    

class Thing(Storable):
    project: ObjectIdField = None
    
    type: ThingType
    implementation: Optional[str] = None
    implementation_version: Optional[str] = None
    revision: int
    
    name: Optional[str] = None
    data: Union[
        StreamData,
        CameraData,
        ModelData,
        LightData,
        CalculationData,
    ]
    
    @pydantic.root_validator(pre=True)
    @classmethod
    def _set_id(cls, data):
        document_id = data.get("_id")
        if document_id:
            data["id"] = document_id
        return data


class AddThingArgs(BaseModel):
    project: ObjectIdField = None
    
    type: ThingType
    
    # Do these belong here?
    implementation: Optional[str] = None
    implementation_version: Optional[str] = None
    
    name: Optional[str] = None
    data: Optional[Json] = None
    
    data: Union[
        StreamData,
        CameraData,
        ModelData,
        LightData,
        CalculationData,
    ]
    
    def create(self) -> Thing:
        return Thing(**self.dict(), revision=0)


class ThingUpdates(BaseModel):
    project: ObjectIdField = None
    
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
    