
from typing import Optional, Tuple

from pydantic import BaseModel, validator
import cv2
import random
import hashlib
from pathlib import Path
import numpy as np


class VCGuard:
    path: str
    cap: cv2.VideoCapture
    frame_count: Optional[int]
    
    def __init__(self, path: Path) -> None:
        self.path = path
        self.cap = cv2.VideoCapture(str(path))
        self.frame_count = None
        
    def __enter__(self) -> cv2.VideoCapture:
        if not self.cap.isOpened():
            raise Exception(f"Error opening video stream or file {self.path}")
        self.frame_count = int(self.cap.get(cv2. CAP_PROP_FRAME_COUNT))
        return self.cap
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.cap.release()
        
    def get_frame(self, frame_no: int) -> np.ndarray:
        if frame_no >= self.frame_count:
            raise Exception(f"Frame out of bounds {frame_no}")
        
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        ret, frame = self.cap.read()
        if not ret:
            raise Exception("Unable to get frame")
        return frame
        



def _calculate_checksum(path: Path) -> str:
    sha256_hash = hashlib.sha256()
    with path.open("rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()


def _get_stat_info(path: Path) -> dict:
    result = path.stat()
    return dict(
        mode=result.st_mode, # int
        inode=result.st_ino, # int
        device=result.st_dev, # int
        size=result.st_size, # int
        modified_time=result.st_mtime,
        # creation_time=result.st_birthtime,
        # filesytem=result.st_fstype,
    )


def _swap(i: int) -> int:
    if i == 0:
        return 1
    elif i == 1:
        return 0
    else:
        return i


def _get_cv_info(path: Path) -> dict:
    guard = VCGuard(path)
    with guard as cap:
        frame_no = random.randint(0, guard.frame_count) #  TODO: LOL
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        shape = guard.get_frame(frame_no)
        revised_shape = tuple(
            shape[_swap(idx)]
            for idx in range(len(shape))
        )
        return dict(
            frame_count=guard.frame_count,
            resolution=revised_shape,
        )


def _get_frame(path: Path, frame_no: int) -> np.ndarray:
    guard = VCGuard(path)
    with guard as cap:
        return guard.get_frame(frame_no)


def _generate_images(path: Path, num_frames: int, frame_count: int):
    guard = VCGuard(path)
    with guard as cap:
        # sorted(np.random.randint(0, frame_count, size=num_frames))
        for image_num in range(num_frames):
            frame_no = random.randint(0, frame_count)
            # print('Reading frame at ' + str(frame_no / float(frame_count)))
            
            yield guard.get_frame(frame_no)

        # print('read image of size ', frame.shape, frame.dtype)
        # # frame = cv2.resize(frame, dsize=(28, 28))
        # # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #
        # path_prefix = 'images/inputs/random_frame_' + str(image_num).zfill(4)
        # cv2.imwrite(path_prefix + '.png', frame)
        #
        # t = tf.constant(frame, dtype=tf.float32)
        # t = (t - 127.5) / 127.5
        # yield t


class VideoInfo(BaseModel):
    path: str
    resolution: Tuple[int, int, int]
    frame_count: int
    checksum: str
    
    mode: int
    inode: int
    device: int
    size: int
    modified_time: int
    url: Optional[str]
    
    @validator('url', always=True)
    def make_url(cls, v, values) -> str:
        checksum = values["checksum"]
        return f"http://localhost:5000/videos/play/{checksum}"
    
    def get_frame(self, frame_no: int) -> np.ndarray:
        if frame_no >= self.frame_count:
            raise Exception("Frame out of range.")
        return _get_frame(self.path, frame_no)

    def generate_images(self, num_frames: int):
        yield from _generate_images(
            self.path, num_frames, self.frame_count)

    @staticmethod
    def from_path(path: Path) -> "VideoInfo":
        return VideoInfo(
            path=str(path),  # TODO
            **_get_cv_info(path),
            **_get_stat_info(path),
            checksum=_calculate_checksum(path),
        )

