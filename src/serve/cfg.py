from pathlib import Path
import pydantic


class BaseSettings(pydantic.BaseSettings):
    class Config:
        env_file = "env"


# class AppSettings(BaseSettings):
#     title: str = "People API"
#     host: str = "0.0.0.0"
#     port: int = 5000
#     log_level: str = "INFO"
#     arrays_root: str = "/work/ProjectsForFun/pgen/videos/arrays/"
#     videos_root: str = "/work/ProjectsForFun/pgen/videos/inputs/"
#     videos_store: str = "/work/ProjectsForFun/pgen/videos/store.yaml"
#     image_root: str = "/work/ProjectsForFun/pgen/videos/images/"

#     class Config(BaseSettings.Config):
#         env_prefix = "APP_"


class APISettings(BaseSettings):
    title: str = "People API"
    host: str = "0.0.0.0"
    port: int = 5000
    log_level: str = "INFO"
    # create Path getters
    arrays_root_path: str = "/work/ProjectsForFun/pgen/videos/arrays/"
    created_videos_root_path: str = "/work/ProjectsForFun/pgen/videos/output/"
    original_videos_root_path: str = "/work/ProjectsForFun/pgen/videos/inputs/"
    image_root_path: str = "/work/ProjectsForFun/pgen/videos/images/"
    
    videos_store: str = "/work/ProjectsForFun/pgen/videos/store.yaml"
    
    def get_arrays_root(self) -> Path:
        return Path(self.arrays_root_path)
    def get_videos_root(self) -> Path:
        return Path(self.original_videos_root_path)
    def get_image_root(self) -> Path:
        return Path(self.image_root_path)

    class Config(BaseSettings.Config):
        env_prefix = "API_"


class MongoSettings(BaseSettings):
    uri: str = "mongodb://127.0.0.1:27017"
    database: str = "synth"
    project_collection: str = "projects"
    thing_collection: str = "things"
    arrays_collection: str = "arrays"
    videos_collection: str = "videos"

    class Config(BaseSettings.Config):
        env_prefix = "MONGO_"


api_settings = APISettings()
# app_settings = AppSettings()
mongo_settings = MongoSettings()