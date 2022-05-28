import pathlib
from typing import List
from fastapi import APIRouter, Request
from fastapi import status as statuscode
from fastapi.responses import StreamingResponse

from serve.exceptions import (
    get_exception_responses,
    NotFoundException,
)
from serve.repositories.video_repo import repository
from common.model.video_info import VideoInfo

from fastapi import Response
from fastapi import Header
from fastapi.responses import FileResponse
# from fastapi.templating import Jinja2Templates

CHUNK_SIZE = 1024*1024
BYTES_PER_RESPONSE = 100000


router = APIRouter(
    prefix="/videos",
    tags=["videos"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/",
    response_model=List[VideoInfo],
    description="List all the available videos",
)
def _list() -> List[VideoInfo]:
    # TODO Filters
    return repository.list()


@router.get(
    "/{checksum}",
    response_model=VideoInfo,
    description="Get a single video by its unique checksum",
    responses=get_exception_responses(NotFoundException),
)
def _get(checksum: str) -> VideoInfo:
    return repository.get(checksum)


@router.patch(
    "/",
    description="Synchronize the video store with the contents on disk",
    status_code=statuscode.HTTP_204_NO_CONTENT,
)
def _sync() -> None:
    repository.synchronize()


# https://github.com/tiangolo/fastapi/issues/1240
@router.get(
    "/{checksum}/frame/{frame_no}",
    description="Get a frame of a video",
    status_code=statuscode.HTTP_200_OK,
)
async def _frame(checksum: str, frame_no: int):
    path = repository.get_image_path(checksum, frame_no)
    return FileResponse(
        path,
        media_type="image/png",
        filename=f"{checksum}_{frame_no:05d}.png")


def chunk_generator_from_stream(path, chunk_size, start, size):
    with open(path, "rb") as stream:
        bytes_read = 0

        stream.seek(start)

        while bytes_read < size:
            bytes_to_read = min(
                chunk_size, size - bytes_read)
            yield stream.read(bytes_to_read)
            bytes_read = bytes_read + bytes_to_read


# https://github.com/tiangolo/fastapi/issues/1240
@router.get(
    "/{checksum}/play",
    description="Play the video",
    status_code=statuscode.HTTP_206_PARTIAL_CONTENT,
)
def stream(checksum: str, req: Request):
    info = repository.get(checksum)
    asked = req.headers.get("Range")

    total_size = info.size
    start_byte_requested = int(asked.split("=")[-1][:-1])
    end_byte_planned = min(start_byte_requested + BYTES_PER_RESPONSE, total_size) - 1
    return StreamingResponse(
        chunk_generator_from_stream(
            info.path,
            chunk_size=10000,
            start=start_byte_requested,
            size=BYTES_PER_RESPONSE),
        status_code=206,
        headers={
            "Accept-Ranges": "bytes",
            "Content-Range": f"bytes {start_byte_requested}-{end_byte_planned}/{total_size}",
            # "Content-Type": "..."
            })