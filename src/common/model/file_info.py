

from enum import Enum, auto
from os import stat, stat_result
from typing import Dict, Optional
from pydantic import Field

from pathlib import Path, PosixPath
import hashlib

from common.model.base import BaseModel


def _calculate_checksum(path: Path) -> str:
    sha256_hash = hashlib.sha256()
    with path.open("rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()


def _get_stat_info(result: stat_result) -> dict:
    return dict(
        mode=result.st_mode, # int
        inode=result.st_ino, # int
        device=result.st_dev, # int
        size=result.st_size, # int
        modified_time=result.st_mtime,
        # creation_time=result.st_birthtime,
        # filesytem=result.st_fstype,
    )


class StatCache(BaseModel):
    cache: Dict[str, Optional[stat_result]] = Field(default_factory=dict)
    
    def get_stat(self, path: Path) -> Optional[stat_result]:
        s = str(path)
        if s not in self.cache:
            try:
                self.cache[s] = path.stat()
            except FileNotFoundError as e:
                self.cache[s] = None
        return self.cache[s]
    
    
class FileInfo(BaseModel):
    path: Path
    checksum: str
    mode: int
    inode: int
    device: int
    size: int
    modified_time: float
    
    def is_dirty(self, cache: StatCache) -> Optional["FileInfo"]:
        stat = cache.get_stat(self.path)
        if stat is None:
            return True
        return (
            stat.st_ino != self.inode or
            stat.st_mtime > self.modified_time
        )

    @staticmethod
    def read_file_info(path: Path, result: Optional[stat_result] = None):
        return FileInfo(
            **_get_stat_info(path.stat() if result is None else result),
            path=str(path),
            checksum=_calculate_checksum(path)
        )

    class Config:
        json_encoders = {PosixPath: str}

