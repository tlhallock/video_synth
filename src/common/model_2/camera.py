from pydantic import Field
from typing import List, Optional, Sequence
from contextlib import suppress
import dateutil
import datetime
import pydantic
from enum import Enum
from typing import List, Optional
import numpy as np
import math

from ..schema.base import BaseModel, FloatingPointType
from ..schema.fields import ProjectFields
from ..schema.person_address import 


__all__ = ("ProjectUpdates", "Project", "Projects", "CreateProjectArgs")


class Resolution(BaseModel):
    width: int
    height: int
    
    def scaled(self):
        return Resolution(
            width=1.0 if self.height > self.width else self.width / self.height,
            height=1.0 if self.width > self.height else self.height / self.width
        )
    
    def copy(self):
        return Resolution(**self.dict())
    
    def nb_pixels(self):
        return self.width * self.height


class Cameras:
    RESOLUTIONS = [
        Resolution(width=352, height=240),
        Resolution(width=350, height=240),
        Resolution(width=720, height=240),
        Resolution(width=640, height=480),
        Resolution(width=720, height=480),
        Resolution(width=960, height=582),
        Resolution(width=1024, height=768),
        Resolution(width=1280, height=720),
        Resolution(width=1024, height=1024),
        Resolution(width=1280, height=800),
        Resolution(width=1366, height=768),
        Resolution(width=1440, height=900),
        Resolution(width=1536, height=864),
        Resolution(width=1920, height=1080),
        Resolution(width=1920, height=1200),
    ]
    
    DEFAULT_RESOLUTION = RESOLUTIONS[3]
    
	@staticmethod
	def print_resolutions():
		for res in Cameras.RESOLUTIONS:
			print(res, res[0] * res[1])


class BaseCamera(BaseModel):
    ftype: FloatingPointType = Field(
        description="The floating point type used to compute an image.",
        default_factory=FloatingPointType.default
    )
    resolution: Resolution = Field(
        description="The output resolution of the camera",
        default_factory=lambda: Cameras.DEFAULT_RESOLUTION.copy()
    )
    
    def nb_pixels(self):
        return self.resolution.nb_pixels()

    def image_shape(self):
        return self.resolution.width, self.resolution.height, 
    
    def depth_shape(self):
        return self.resolution.width, self.resolution.height
    
    def image_format(self):
        pass


class PinholeCamera(BaseCamera):
    z_near: float = 0.1
    z_far: float = 100
    tan_fov: float = np.tan(0.25 * math.pi)

    # @functools.cache
    def construct_transformed_projection(self):
        scaled = self.resolution.scaled()
        x_scale, y_scale = scaled.width, scaled.height

        tan_fov_x = x_scale * self.tan_fov
        tan_fov_y = y_scale * self.tan_fov

        nr, fr = self.z_near[0], self.z_far[1]

        z = np.zeros((1,), dtype=self.ftype.to_np())
        o = np.ones((1,), dtype=self.ftype.to_np())

        a = fr / (fr - nr)
        b = -nr * fr / (fr - nr)
        x = o / tan_fov_x
        y = o / tan_fov_y

        transform = np.block([
            [x, z, z, z],
            [z, y, z, z],
            [z, z, a, b],
            [z, z, o, z],
        ])
        return transform

    # @functools.cache
    def linear_components(self):
        # pixel = b + m * idx
        w, h = self.resolution.width, self.resolution.height
        bx, by = -1 + 0.5 / w, -1 + 0.5 / h
        ex, ey = +1 - 0.5 / w, +1 - 0.5 / h

        return np.array([
            [bx, by],
            [(ex - bx) / (w - 1), (ey - by) / (h - 1)]
        ], self.ftype)

        # @functools.cache
        # def projected_coords(self):
        #     xs = np.linspace(-1 + 0.5 / self.width(), 1 - 0.5 / self.width(), self.width())
        #     ys = np.linspace(-1 + 0.5 / self.height(), 1 - 0.5 / self.height(), self.height())
        #     return xs, ys

        # @functools.cache
        # def projected_rays(self):
        #     xs, ys = self.projected_coords()
        #     pixels = np.array([
        #         [
        #             [row, col]
        #             for col in ys
        #         ]
        #         for row in xs
        #     ], dtype=self.ftype)

        #     pixels = np.reshape(pixels, (-1, 1, 2))
        #     nb_pixels = pixels.shape[0]
        #     return np.concatenate([
        #         np.concatenate([pixels, np.full((nb_pixels, 1, 1), self.z_bounds[0])], axis=2),
        #         np.concatenate([pixels, np.full((nb_pixels, 1, 1), self.z_bounds[1])], axis=2)
        #     ], axis=1)
    
    
    



class AddCameraArgs(BaseModel):
    resolution: Optional[Resolution]
    name: Optional[str] = Field(
        description="Optional name of the camera",
        example="camera 1",
    )
    


class ProjectUpdates(BaseModel):
    name: Optional[str] = ProjectFields.name
    address: Optional[Address] = ProjectFields.address_update
    birth: Optional[datetime.date] = ProjectFields.birth

    def dict(self, **kwargs):
        # The "birth" field must be converted to string (isoformat) when exporting to dict (for Mongo)
        # TODO Better way to do this? (automatic conversion can be done with Config.json_encoders, but not available for dict
        d = super().dict(**kwargs)
        with suppress(KeyError):
            d["birth"] = d.pop("birth").isoformat()
        return d


class Project(BaseModel):
    project_id: str = ProjectFields.project_id
    name: str = ProjectFields.name
    age: Optional[int] = ProjectFields.age
    created: int = ProjectFields.created
    updated: int = ProjectFields.updated

    @pydantic.root_validator(pre=True)
    @classmethod
    def _set_project_id(cls, data):
        document_id = data.get("_id")
        if document_id:
            data["project_id"] = document_id
        return data

    @pydantic.root_validator()
    @classmethod
    def _set_age(cls, data):
        birth = data.get("birth")
        if birth:
            today = datetime.datetime.now().date()
            data["age"] = dateutil.relativedelta.relativedelta(today, birth).years
        return data

    class Config(BaseModel.Config):
        extra = pydantic.Extra.ignore  # if a read document has extra fields, ignore them


Projects = List[Project]






class CameraType(Enum):
    PINHOLE_CAMERA = 'PINHOLE'


class CameraType