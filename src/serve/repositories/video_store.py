
from typing import Dict, List
from pydantic import BaseModel, Field
from common.model.video_info import VideoInfo
from random import Random
import yaml
import os
from pathlib import Path

from serve import cfg
import cv2


def _is_video(filename) -> bool:
    for ext in ['.mp4', '.mkv']:
        if filename.endswith(ext):
            return True
    for ext in ['.nfo', 'html']:
        if filename.endswith(ext):
            return False
    print('Ignoring "', filename, '"')
    return False


def _scan(root: str):
    for root, _, files in os.walk(root, topdown=False):
        for file in files:
            if not _is_video(file):
                continue
            p = os.path.join(root, file)
            print(f"Found video file '{p}'")
            yield Path(p)


class VideoStore(BaseModel):
    videos: Dict[str, VideoInfo] = Field(default_factory=dict)

    def get_random_video(self, random: Random) -> VideoInfo:
        if len(self.videos) == 0:
            raise Exception("No videos.")
        video_index = random.randint(0, len(self.videos) - 1)
        return self.videos[video_index]
    
    def synchronize(self, path: str):
        print(self.videos)
        # Get all the videos that might be updated removed
        # do a scan, but do not update files that have not been touched since they were registered
        # Remove files that no longer exist
        pass

    # TODO: Move
    def save(self, path) -> None:
        with open(path, 'w') as file:
            yaml.dump(self.dict(), file)
    
    # TODO: Move
    @staticmethod
    def load(path) -> "VideoStore":
        with open(path, 'r') as fin:
            y = yaml.full_load(fin)
        return VideoStore(**y)

    @staticmethod
    def from_root(root: str) -> "VideoStore":
        map = dict()
        for path in _scan(root):
            info = VideoInfo.from_path(path)
            map[info.info.checksum] = info
        return VideoStore(videos=map)

    @staticmethod
    def get_store(videos_file: str, directory_path: str) -> "VideoStore":
        try:
            return VideoStore.load(videos_file)
        except:
            store = VideoStore.from_root(directory_path)
            store.save(videos_file)
            return store


class ImageCache(BaseModel):
    # cached_list: List[str] = Field(default_factory=list)
    # max_images: int = 8192
    root_dir: Path
    
    def get_path(self, info: VideoInfo, frame_no: int) -> Path:
        parent = self.root_dir / info.checksum
        p = parent / (str(frame_no) + ".png")
        if not p.exists():
            if not parent.exists():
                Path.mkdir(
                    parent,
                    parents=True,
                    exist_ok=True)
            frame = info.get_frame(frame_no)
            cv2.imwrite(str(p), frame)
        return p
        


class VideoRepository(BaseModel):
    root_path: str
    store_path: str
    store: VideoStore
    cache: ImageCache
    
    def synchronize(self) -> None:
        self.store.synchronize(self.root_path)
        self.store.save(self.store_path)
        
    def list(self) -> List[VideoInfo]:
        return [nfo for nfo in self.store.videos.values()]
    
    def get(self, checksum: str) -> VideoInfo:
        return self.store.videos[checksum]
    
    def get_image_path(self, checksum: str, frame_no: int) -> str:
        return self.cache.get_path(
            self.get(checksum), frame_no)


repository = VideoRepository(
    root_path=(root_path := str(cfg.api_settings.get_videos_root())),
    store_path=(store_path := cfg.api_settings.videos_store),
    cache=ImageCache(
        root_dir=cfg.api_settings.get_image_root()),
    store=VideoStore.get_store(
        store_path,
        root_path))