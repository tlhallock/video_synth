from enum import Enum, unique
from pathlib import Path
from typing import Any, Dict
from bson import ObjectId
from numpy import isin
import pydantic
import pathlib


from common.utils.utils import get_time, create_uuid


def _patch_value(key: str, value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, ObjectId):
        return str(value)
    
    from common.model.thing import ThingType, StreamType
    if isinstance(value, Enum):
        return value.value
    # Patch up the datetime object...
    return value


def revise_dict(d: Dict[str, Any]) -> Dict[str, Any]:
    return {
        key: _patch_value(key, value)
        for key, value in d.items()
    }


class BaseModel(pydantic.BaseModel):
    """All data models inherit from this class"""

    # @pydantic.root_validator(pre=True)
    # def _min_properties(cls, data):
    #     """At least one property is required"""
    #     if not data:
    #         raise ValueError("At least one property is required")
    #     return data

    # def dict(self, include_nulls=False, **kwargs):
    #     """Override the super dict method by removing null keys from the dict, unless include_nulls=True"""
    #     kwargs["exclude_none"] = not include_nulls
    #     return super().dict(**kwargs)
    
    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        return revise_dict(super().dict(*args, **kwargs))

    class Config:
        json_encoders = {
            ObjectId: str
        }
        # TODO:
        # extra = pydantic.Extra.forbid  # forbid sending additional fields/properties
        anystr_strip_whitespace = True  # strip whitespaces from strings


@unique
class FloatingPointType(Enum):
    Float64 = "64"
    Float32 = "32"
    
    def to_np(self):
        import numpy as np
        if self.name == "Float64":
            return np.float64
        elif self.name == "Float32":
            return np.float32
        else:
            raise Exception()
    
    @classmethod
    def default(cls):
        return cls.Float32


class Fields:
    unix_ts = dict(
        description="Unix timestamp",
        example=get_time(),
    )

    identifer = dict(
        description="Unique identifier",
        example=create_uuid(),
        min_length=36,
        max_length=36,
    )
