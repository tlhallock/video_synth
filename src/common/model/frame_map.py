





from typing import List, Optional
from pydantic import BaseModel


class MapSegment(BaseModel):
    src: int
    dst: int
    length: Optional[int] = None
    step: int = 1


class FrameMap(BaseModel):
    segments: List[MapSegment]