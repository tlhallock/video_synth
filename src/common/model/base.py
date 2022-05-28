from enum import Enum, unique
import pydantic

from common.utils import get_time, create_uuid

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

    class Config:
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
