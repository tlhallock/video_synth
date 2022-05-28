from pathlib import Path
import yaml
import os

import torch
from model import MattingNetwork
from inference import convert_video

from common.unit_of_work import UnitOfWork
from common.args import create_parser
from common.default_logging import get_logger


logger = get_logger(__name__)


def process_video(model: MattingNetwork, input_file: Path, output_directory: Path):
    logger.info(
        f"Processing {str(input_file)} to {str(output_directory)}")
    
    params = {
        'mbps': 4
    }

    # print('processing', input_file, 'to', output_directory)
    # print('\tbeginning at', datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    convert_video(
        model,                           # The model, can be on any device (cpu or cuda).
        input_source=input_file,        # A video file or an image sequence directory.
        output_type='video',             # Choose "video" or "png_sequence"
        output_composition=str(output_directory / 'composition.mp4'),
        output_alpha=str(output_directory / 'alpha.mp4'),
        output_foreground=str(output_directory / 'foreground.mp4'),
        output_video_mbps=params['mbps'],
        downsample_ratio=None,
        seq_chunk=12,  # Process n frames at once for better parallelism.
    )
    print("Done.")
    # print('\tcompleted at', datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))

    info_path = output_directory / "info.yaml"
    with info_path.open("w") as outf:
        yaml.dump(
            {
                'params': params,
                'input-path': input_file,
                'output-path': output_directory,
                'info-file': info_path,
                # 'path-hash': path_hash,
                'completed': True
            },
            outf)


def main():
    parser = create_parser()
    # parser.add_argument(
    #     "-r", "--resnet",
    #     dest="resnet",
    #     help="Resnet path",
    #     required=True,
    #     type=str)
    args = parser.parse_args()
    uow = UnitOfWork.parse_args(args)
    
    model = MattingNetwork('resnet50').eval().cuda()
    resnet_path = os.environ.get("RESNET_PATH", "rvm_resnet50.pth")
    model.load_state_dict(torch.load(resnet_path))
    
    for input_file in uow.input_files():
        process_video(model, input_file, uow.get_output_directory())
