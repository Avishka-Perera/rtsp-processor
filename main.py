from multiprocessing import JoinableQueue, Process
from rtsp_processor.stream.process import process_job
from rtsp_processor.stream.stream import stream_job
import yaml
from argparse import ArgumentParser
import os
import sys

sys.path.append(os.getcwd())


def parse_args():
    parser = ArgumentParser()
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

    root = os.path.split(__file__)[0]
    config_path = os.path.abspath(os.path.join(root, args.config_path))
    with open(config_path) as handler:
        config = yaml.load(handler, yaml.FullLoader)

    image_queue = JoinableQueue()

    producer = Process(target=process_job, args=(image_queue, config))
    consumer = Process(target=stream_job, args=(image_queue, config, args.backend))

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()
