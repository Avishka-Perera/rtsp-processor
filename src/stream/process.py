import cv2 as cv
from multiprocessing import JoinableQueue
from typing import Dict
from ..util import make_obj_from_conf


def process_job(queue: JoinableQueue, config: Dict) -> None:
    source_url = config["source_stream"]["url"]
    batch_size = config["batch_size"]
    processor_conf = config["processor"]
    processor = make_obj_from_conf(processor_conf)
    capture = cv.VideoCapture(source_url)
    img_batch = []
    while True:
        grabbed, frame = capture.read()
        if not grabbed:
            break

        img_batch.append(frame)
        if len(img_batch) >= batch_size:
            proc_batch = processor(img_batch)
            queue.put(proc_batch)
            img_batch = []
