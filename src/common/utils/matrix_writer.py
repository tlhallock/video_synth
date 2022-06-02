
from multiprocessing.dummy import Array
from pathlib import Path
from typing import Any, List, Optional, Sequence
import numpy as np

from pydantic import BaseModel, Field

from common.model.file_info import FileInfo, StatCache


class MatrixWriter(BaseModel):
    block_size: int
    root: Path
    prefix: str = "array"
    
    mat_shape: Optional[Sequence[int]] = None
    mat_dtype: Optional[Any] = None
    
    mats: List[np.ndarray] = Field(default_factory=list)
    paths: List[Path] = Field(default_factory=list)
    count: int = 0
    
    
    def get_shape(self) -> Sequence[int]:
        return tuple(
            [self.count] + [d for d in self.mat_shape])
        
    def get_infos(self) -> List[FileInfo]:
        cache = StatCache()
        return [
            FileInfo.read_file_info(path, cache)
            for path in self.paths
        ]
    
    # enter/exit
    
    def _assert(self, mat: np.ndarray) -> None:
        if self.mat_dtype is None:
            self.mat_dtype = mat.dtype
        else:
            assert self.mat_dtype == mat.dtype
        if self.mat_shape is None:
            self.mat_shape = mat.shape
        else:
            assert self.mat_shape == mat.shape
    
    def write(self):
        if len(self.mats) > 0:
            outpath=self.root / f"{self.prefix}_{self.count:05d}.npy"
            np.save(
                file=outpath,
                arr=np.array(self.mats, dtype=np.float64),  # TODO
                allow_pickle=False,
                fix_imports=False)
            self.count += 1
            self.paths.append(outpath)
        self.mats.clear()
    
    def receive(self, mat: np.ndarray):
        self._assert(mat)
        self.mats.append(mat)
        if len(self.mats) > self.block_size:
            self.write()
        
    class Config:
        arbitrary_types_allowed = True
