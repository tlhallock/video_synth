from typing import List
import numpy as np
from pydantic import BaseModel, Field
import cv2 as cv

from pathlib import Path
import yaml
import os
from tqdm import tqdm

from calc.common.unit_of_work import UnitOfWork
from calc.common.args import create_parser
from calc.common.default_logging import get_logger


logger = get_logger(__name__)


class FarnebackParams(BaseModel):
    block_size: int


class MatWriter(BaseModel):
    block_size: int
    root: Path
    suffix: str = "matrix"
    
    mats: List[np.ndarray] = Field(default_factory=list)
    paths: List[Path] = Field(default_factory=list)
    count: int = 0
    
    # enter/exit
    
    def write(self):
        if len(self.mats) > 0:
            outpath=self.root / f"{self.count:05d}_{self.suffix}.npy"
            np.save(
                file=outpath,
                arr=np.array(self.mats, dtype=np.float64),  # TODO
                allow_pickle=False,
                fix_imports=False)
            self.count += 1
            self.paths.append(outpath)
        self.mats.clear()
    
    def receive(self, mat: np.ndarray):
        self.mats.append(mat)
        if len(self.mats) > self.block_size:
            self.write()
        
    class Config:
        arbitrary_types_allowed = True
    


def process_video(params: FarnebackParams, input_file: Path, output_directory: Path) -> None:
    logger.info(
        f"Processing {str(input_file)} to {str(output_directory)}")
    
    cap = cv.VideoCapture(str(input_file))
    ret, frame1 = cap.read()
    num_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    
    prvs = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame1)
    hsv[..., 1] = 255
    
    writer = MatWriter(
        block_size=params.block_size,
        root=output_directory,
        suffix="flow")
    
    h, w, _ = frame1.shape
    fourcc = cv.VideoWriter_fourcc('m', 'p', '4', 'v')
    video_writer = cv.VideoWriter(
        str(output_directory / "both.mp4"),
        fourcc,
        30,
        (2 * w, h))
    
    for f_no in tqdm(range(num_frames - 1)):
        ret, frame2 = cap.read()
        if not ret:
            logger.warn(f"No frame grabbed. {f_no}")
            break
        
        next = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
        # https://docs.opencv.org/3.4/dc/d6b/group__video__track.html#ga5d10ebbd59fe09c5f650289ec0ece5af
        flow = cv.calcOpticalFlowFarneback(
            prev=prvs, 
            next=next,
            flow=None,
            pyr_scale=0.5,
            levels=3,
            winsize=15,
            iterations=3,
            poly_n=5, 
            poly_sigma=1.2,
            flags=0)
        
        writer.receive(flow)
        
        mag, ang = cv.cartToPolar(flow[..., 0], flow[..., 1])
        hsv[..., 0] = ang*180/np.pi/2
        hsv[..., 2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)
        bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
        
        both = cv.hconcat([frame2, bgr])
        video_writer.write(both)
        
        # cv.imwrite(str(output_directory / f"{f_no:04d}_both.png"), both)
        # cv.imwrite(str(output_directory / f"{f_no:04d}_opticalfb.png"), frame2)
        # cv.imwrite(str(output_directory / f"{f_no:04d}_opticalhsv.png"), bgr)
        prvs = next
    
    video_writer.release()
    writer.write()
    # cap.release()

    info_path = output_directory / "info.yaml"
    with info_path.open("w") as outf:
        yaml.dump(
            stream=outf,
            data={
                'computation': 'optical-flow',
                'implementation': 'farneback',
                'params': params.dict(),
                'output-type': 'matrix',
                'matrix-paths': [str(p) for p in writer.paths],
                'input-path': str(input_file),
                'output-path': str(output_directory),
                'info-file': str(info_path),
                'completed': True})


def main():
    parser = create_parser()
    parser.add_argument(
        "-b", "--block-size", 
        dest="block_size",
        type=int,
        default=64)
    args = parser.parse_args()
    uow = UnitOfWork.parse_args(args)
    
    for input_file in uow.input_files():
        process_video(
            params=FarnebackParams(block_size=args.block_size),
            input_file=input_file,
            output_directory=uow.get_output_directory())
    



