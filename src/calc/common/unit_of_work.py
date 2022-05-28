

from email.generator import Generator
from typing import Optional
from pydantic import BaseModel
from pathlib import Path
from common.args import create_parser
import os

import glob


class UnitOfWork(BaseModel):
    input_video: Optional[Path]
    input_glob: Optional[str]
    output_directory: Path
    
    def ensure_output(self) -> None:
        os.makedirs(self.output_directory, exist_ok=True)
    
    def get_output_directory(self) -> Path:
        self.ensure_output()
        return self.output_directory
    
    def input_files(self): #  -> Generator[Path]:
        if self.input_video is not None:
            yield self.input_video
        if self.input_glob is not None:
            for video in glob.glob(self.input_glob):
                yield video
            
    
    @staticmethod
    def parse_args(args) -> "UnitOfWork":
        uow = UnitOfWork(
            input_video=Path(args.input_video),
            input_glob=None,
            output_directory=Path(args.output_directory))
        return uow

