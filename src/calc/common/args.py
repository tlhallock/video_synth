import argparse

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Process a video")
    parser.add_argument(
        "-i", "--input-video",
        dest="input_video",
        help="Input video",
        required=True,
        type=str)
        # type=argparse.FileType("r"))
    parser.add_argument(
        "-o", "--output-directory",
        dest="output_directory",
        help="directory to write output",
        required=True,
        type=str # path
    )
    return parser
