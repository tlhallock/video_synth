
from random import Random
from typing import Any, Dict, List

from pathlib import Path
from common.model.video_info import VideoInfo

from serve.database import db
from serve.repositories.fs_repo import FileSystemRepo
from common.model.base import BaseModel
from common.model.file_info import StatCache
from serve import cfg

import cv2

from serve.exceptions import NotFoundException
from serve.cfg import mongo_settings

# These should be deleted when the project is deleted...


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


class VideosRepository(FileSystemRepo[VideoInfo]):
    image_cache: ImageCache
    
    def __init__(self, database, desc: str, root: Path, globs: List[str], image_cache: ImageCache):
        super().__init__(database, desc, root, globs)
        self.image_cache = image_cache
    
    # def construct(self, data: Dict[str, Any]) -> VideoInfo:
    #     id = data["_id"]
    #     del data["_id"]
    #     return VideoInfo(**data, id=id)
    
    def create_document(self, path: Path, cache: StatCache) -> VideoInfo:
        return VideoInfo.from_path(path, cache)
    
    def get_by_checksum(self, checksum: str) -> VideoInfo:
        document = self.collection.find_one({"info.checksum": {"$eq": checksum}})
        if not document:
            raise NotFoundException(f"Unable to find {self.desc} {id}")
        return self.construct(document)
        # self.collection.find(dict())
        # return self.store.videos[checksum]
    
    def get_random_video(self, random: Random) -> VideoInfo:
        # if len(self.videos) == 0:
        #     raise Exception("No videos.")
        # video_index = random.randint(0, len(self.videos) - 1)
        # return self.videos[video_index]
        raise Exception("Implement me!")
    
    def get_image_path(self, checksum: str, frame_no: int) -> str:
        return self.image_cache.get_path(
            self.get_by_checksum(checksum), frame_no)
        
    class Meta:
        collection_name = mongo_settings.videos_collection
    

repository: VideosRepository = VideosRepository(
    database=db,
    root=cfg.api_settings.get_videos_root(),
    globs=["**/*.mp4", "**/*.mkv"],
    desc="video",
    image_cache=ImageCache(
        root_dir=cfg.api_settings.get_image_root()),
)
