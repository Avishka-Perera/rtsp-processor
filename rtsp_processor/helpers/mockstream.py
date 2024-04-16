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
from rtsp_processor.stream.streamer import Streamer


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
        "--crop-shape",
        type=ast.literal_eval,
        nargs="+",
        help="Size (height, width) of the images to perform the initial center crop",
        default=[370, 1224],
    )
    parser.add_argument(
        "-s",
        "--resize-shape",
        type=ast.literal_eval,
        nargs="+",
        help="Size (height, width) of the images to perform the resizing",
        default=[256, 832],
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

    root = os.path.join(os.path.split(__file__)[0], os.pardir, os.pardir)
    config_path = os.path.abspath(os.path.join(root, args.config_path))
    with open(config_path) as handler:
        config = yaml.load(handler, yaml.FullLoader)

    fps = config["fps"]
    sink_url = config["source_stream"]["url"]
    crop_hw = args.crop_shape
    resize_hw = args.resize_shape
    imgs_dir = os.path.abspath(os.path.join(root, args.image_dir))

    streamer = Streamer(sink_url, fps, resize_hw, args.backend)

    start = time()
    published_count = 0

    img_lst = sorted(glob.glob(f"{imgs_dir}/**"))
    if len(img_lst) == 0:
        raise FileNotFoundError(f"No images foung under '{imgs_dir}'")

    while True:
        for i, img_path in enumerate(img_lst):

            img = Image.open(img_path)
            orig_hw = img.size[::-1]
            top = int((orig_hw[0] - crop_hw[0]) / 2)
            bottom = top + crop_hw[0]
            left = int((orig_hw[1] - crop_hw[1]) / 2)
            right = left + crop_hw[1]
            frame = np.array(
                img.crop((left, top, right, bottom)).resize(resize_hw[::-1])
            ).astype(np.uint8)

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
