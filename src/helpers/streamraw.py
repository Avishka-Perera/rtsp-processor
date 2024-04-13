import glob
from time import sleep, time
import cv2
import numpy as np
from PIL import Image
import yaml
from argparse import ArgumentParser
import ast


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
    args = parser.parse_args()
    return args


if __name__ == "__main__":

    args = parse_args()
    with open("./config.yaml") as handler:
        config = yaml.load(handler, yaml.FullLoader)

    fps = config["fps"]
    sink_url = config["source_stream"]["url"]
    width, height = args.size
    imgs_dir = args.image_dir

    out = cv2.VideoWriter(
        "appsrc ! videoconvert"
        + " ! video/x-raw,format=I420"
        + " ! x264enc speed-preset=ultrafast bitrate=600 key-int-max="
        + str(fps * 2)
        + " ! video/x-h264,profile=baseline"
        + f" ! rtspclientsink location={sink_url}",
        cv2.CAP_GSTREAMER,
        0,
        fps,
        (width, height),
        True,
    )
    if not out.isOpened():
        raise Exception("can't open video writer")

    curcolor = 0
    start = time()

    img_lst = sorted(glob.glob(f"{imgs_dir}/**"))

    while True:
        for img_path in img_lst:
            frame = np.array(Image.open(img_path).resize((width, height))).astype(
                np.uint8
            )[:, :, ::-1]

            out.write(frame)

            now = time()
            diff = (1 / fps) - now - start
            if diff > 0:
                sleep(diff)
            start = now
