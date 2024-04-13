from multiprocessing import JoinableQueue, Process
from src.stream.process import process_job
from src.stream.stream import stream_job
import yaml
from argparse import ArgumentParser


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
    with open(args.config_path) as handler:
        config = yaml.load(handler, yaml.FullLoader)

    image_queue = JoinableQueue()

    producer = Process(target=process_job, args=(image_queue, config))
    consumer = Process(target=stream_job, args=(image_queue, config, args.backend))

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()
