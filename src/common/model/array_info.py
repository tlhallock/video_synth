
from enum import Enum, auto
from typing import List, Optional
from pydantic import BaseModel, Field
from common.schema.fields import Details


class DataType(Enum):
    Uint8 = auto
    Int32 = auto
    Int64 = auto
    Float32 = auto
    Float64 = auto
    

class ArrayInfo(BaseModel):
    id: str = Field(**Details.identifer)
    thing: str = Field(**Details.identifer)
    created: int = Field(**Details.unix_ts) #, default_factory=get_time)
    updated: int = Field(**Details.unix_ts) #, default_factory=get_time)
    
    variable_path: str
    interpretation: Optional[str] = None
    # Distinguish between euler angles/quaternions
    
    shape: List[int]
    dtype: DataType
    root_path: str
    block_size: int

