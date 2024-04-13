from multiprocessing import JoinableQueue
import queue
import cv2
from typing import Dict
from .streamer import Streamer


def stream_job(image_queue: JoinableQueue, config: Dict, backend: str):
    fps = config["fps"]
    sink_url = config["sink_stream"]["url"]
    size = config["sink_stream"]["size"]
    width, height = size
    streamer = Streamer(sink_url, fps, size, backend)

    while True:
        try:
            image = image_queue.get(timeout=5)[0]
            if image is None:
                break

            image = cv2.resize(image, (width, height))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            streamer(image)

            image_queue.task_done()
        except queue.Empty:
            pass

    streamer.close()
