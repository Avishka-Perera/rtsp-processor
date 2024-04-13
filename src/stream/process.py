import cv2 as cv
from multiprocessing import JoinableQueue
from ..helpers.my_processor import MyProcessor
from typing import Dict
from ..util import make_obj_from_conf


def process_job(
    queue: JoinableQueue,
    config: Dict,
    batch_sz: int = 1,
) -> None:
    source_url = config["source_stream"]["url"]
    processor = make_obj_from_conf(config["processor"])
    capture = cv.VideoCapture(source_url)
    img_batch = []
    while True:
        grabbed, frame = capture.read()
        if not grabbed:
            break
        if len(img_batch) <= batch_sz:
            img_batch.append(frame)
        else:
            antt_img_batch = processor(img_batch)
            queue.put(antt_img_batch)
            img_batch = [frame]
