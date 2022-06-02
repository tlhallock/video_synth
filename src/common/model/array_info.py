
from enum import Enum, auto
from pathlib import Path
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
import yaml
import numpy as np

from common.model.file_info import FileInfo, StatCache
from common.model.fs_resource import MultiFileResource

from serve.cfg import api_settings

from common.model.base import Fields
from common.utils.matrix_writer import MatrixWriter
from pydantic_mongo import ObjectIdField


class DataType(Enum):
    Uint8 = "uint8"
    Int32 = "int32"
    Int64 = "int64"
    Float32 = "float32"
    Float64 = "float64"



class ArrayInfo(MultiFileResource):
    thing: ObjectIdField
    
    variable_path: str
    interpretation: Optional[str] = None
    # Distinguish between euler angles/quaternions
    
    shape: List[int]
    dtype: DataType
    root_path: str
    block_size: int
    
    def open(self):
        return MatrixWriterGuard.open(self)
    
    @staticmethod
    def create_document(self, path: Path, cache: StatCache) -> "ArrayInfo":
        with open(path / "info.yaml") as infile:
            y = yaml.load_all(infile)
            prev = ArrayInfo(**y)
        return prev


class CreateArrayInfo(BaseModel):
    thing: str = Field(**Fields.identifer)
    variable_path: str
    shape: List[int]
    dtype: DataType
    
    interpretation: Optional[str] = None
    block_size: Optional[int] = 512
    
    def creation_data(self) -> Dict[str, Any]:
        return dict(
            **self.dict(),
            path=Path(api_settings.arrays_root) / "",
            infos=[],
            glob="array_*.npz",
        )





class MatrixWriterGuard:
    def __init__(self, array: ArrayInfo, writer: MatrixWriter) -> None:
        self.array = array
        self.writer = writer
        
    def __enter__(self) -> MatrixWriter:
        return self.writer
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.writer.write()
        
        self.array.shape = self.writer.get_shape()
        self.array.infos = self.writer.get_infos()
        self.array.block_size = self.writer.block_size
        self.array.dtype = self.writer.mat_dtype
        
        with open(self.array.path / "info.yaml", "w") as outfile:
            yaml.dump(self.array, outfile)
        
    
    @staticmethod
    def open(array: ArrayInfo) -> "MatrixWriterGuard":
        return MatrixWriterGuard(
            array=array,
            writer=MatrixWriter(
                block_size=array.block_size,
                root=array.root_path,
                # prefix=,
                # mat_shape=,
                # mat_dtype=,
            )
        )
