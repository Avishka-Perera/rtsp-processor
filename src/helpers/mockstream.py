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
        default="./data/images",
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

    start = time()
    published_count = 0

    img_lst = sorted(glob.glob(f"{imgs_dir}/**"))

    while True:
        for i, img_path in enumerate(img_lst):
            frame = np.array(Image.open(img_path).resize((width, height))).astype(
                np.uint8
            )

            streamer([frame])
            published_count += 1

            now = time()
            next_time = start + published_count / fps
            diff = next_time - now
            if diff > 0:
                sleep(diff)

            print(
                f"\rframe: {published_count}       fps: {published_count/(now-start)}",
                end="",
            )

    streamer.close()
