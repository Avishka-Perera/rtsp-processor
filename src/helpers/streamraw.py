import sys
import os

root_dir = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root_dir)

import glob
from time import sleep, time
import numpy as np
from PIL import Image
import yaml
from argparse import ArgumentParser
import ast
from src.stream.streamer import Streamer


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "-i",
        "--image-dir",
        type=str,
        default="./images",
        help="The directory that contains the images to be streamed",
    )
    parser.add_argument(
        "-s",
        "--size",
        type=ast.literal_eval,
        nargs="+",
        help="Size (width, height) of the images in the stream",
        default=[640, 480],
    )
    parser.add_argument(
        "-b",
        "--backend",
        type=str,
        default="opencv",
        choices=["opencv", "ffmpeg"],
        help="Backend to be used for streaming",
    )
    parser.add_argument(
        "-c",
        "--config-path",
        type=str,
        default="./config.yaml",
        help="Path for the config file",
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":

    args = parse_args()
    with open(args.config_path) as handler:
        config = yaml.load(handler, yaml.FullLoader)

    fps = config["fps"]
    sink_url = config["source_stream"]["url"]
    size = args.size
    width, height = size
    imgs_dir = args.image_dir

    streamer = Streamer(sink_url, fps, size, args.backend)

    curcolor = 0
    start = time()

    img_lst = sorted(glob.glob(f"{imgs_dir}/**"))

    while True:
        for i, img_path in enumerate(img_lst):
            frame = np.array(Image.open(img_path).resize((width, height))).astype(
                np.uint8
            )

            print(f"\rframe: {i}", end="")
            streamer(frame)

            now = time()
            diff = (1 / fps) - now - start
            if diff > 0:
                sleep(diff)
            start = now

    streamer.close()
