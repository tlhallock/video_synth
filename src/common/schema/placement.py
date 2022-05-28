# from optparse import Option
# from pydantic import Field, Json
# from typing import List, Optional, Sequence
# from contextlib import suppress
# import dateutil
# import datetime
# import pydantic
# from enum import Enum
# from typing import List, Optional
# import numpy as np
# import math

# from src.common.utils import get_uuid

# from .base import BaseModel, FloatingPointType
# from .fields import Details, ProjectFields
# from .person_address import 


# __all__ = ("ProjectUpdates", "Project", "Projects", "CreateProjectArgs")


# class CreateThing(BaseModel):
#     project_id = Field(**Details.identifer)
    
#     category: str
#     type: str
#     model_version: str
#     name: Optional[str]
#     params: Json
    

# class Thing(BaseModel):
#     id = Field(**Details.identifer)
#     project_id = Field(**Details.identifer)
    
#     category: str
#     type: str
#     model_version: str
#     name: Optional[str]
#     params: Json  # Could be a union of currently supported types

#     @pydantic.root_validator(pre=True)
#     @classmethod
#     def _set_id(cls, data):
#         document_id = data.get("_id")
#         if document_id:
#             data["id"] = document_id
#         return data


# class Placement(BaseModel):
#     frames: Optional[List[int]]
#     begin_frame: Optional[int]
    
#     # Dimensions: frame x 3(x/y/z)
#     world_translation: np.ndarray
#     # Dimensions: frame x 4(quaternion)
#     world_rotation: np.ndarray
#     # Scaling
    
#     # Dimension: frame x # pose params
#     pose: Optional[np.ndarray]


# class ScenePlacement(BaseModel):
#     scene_id: Field(**Details.identifer)
#     thing_id: Field(**Details.identifer)
#     placement: Placement


# class Place(BaseModel):
#     scene_id: Field(**Details.identifer)
#     thing_id: Field(**Details.identifer)
#     placement: Placement
    
#     overwrite: Optional[bool] = False
    