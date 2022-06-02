from typing import Any, Dict, List

import requests

from client.base import BaseClient

from common.model.video_info import VideoInfo
from common.model.fs_resource import SynchonizeResult
import numpy as np


class VideosClient(BaseClient[VideoInfo]):
    def constructor(self, js: Dict[str, Any]) -> VideoInfo:
        return VideoInfo(**js)
    
    def synchronize_entry(self) -> SynchonizeResult:
        pass
    
    def synchronize(self) -> SynchonizeResult:
        r = requests.patch(
            f"{self.get_route()}")
        if r.status_code not in [200]:
            raise Exception(
                f"Recieved unexpected code {r.status_code}.\n {r.content}"
            )
        return SynchonizeResult(**r.json())
    
    def get_frame(self, checksum: str) -> np.ndarray:
        pass
    
    def list_under_project(self, project: str) -> List[VideoInfo]:
        override = f"projects/{project}/things"
        return self.list(override=override)
    
    @staticmethod
    def create_client() -> "VideosClient":
        return VideosClient(
            endpoint="http://localhost:5000",
            route="videos",
        )
