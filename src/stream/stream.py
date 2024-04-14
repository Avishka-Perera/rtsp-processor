from multiprocessing import JoinableQueue
import queue
from typing import Dict
from .streamer import Streamer


def stream_job(image_queue: JoinableQueue, config: Dict, backend: str):
    fps = config["fps"]
    sink_url = config["sink_stream"]["url"]
    size = config["sink_stream"]["size"]
    streamer = Streamer(sink_url, fps, size, backend)

    while True:
        try:
            img_batch = image_queue.get(timeout=5)
            if img_batch is None:
                break
            streamer(img_batch)
            image_queue.task_done()
        except queue.Empty:
            pass

    streamer.close()
