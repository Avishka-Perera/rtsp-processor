import cv2 as cv
from multiprocessing import JoinableQueue
from ..helpers.my_processor import MyProcessor
from typing import Dict


def process_job(
    queue: JoinableQueue,
    config: Dict,
    batch_sz: int = 1,
) -> None:
    source_url = config["source_stream"]["url"]
    model = MyProcessor("bar")
    capture = cv.VideoCapture(source_url)
    img_batch = []
    while True:
        grabbed, frame = capture.read()
        if not grabbed:
            break
        if len(img_batch) <= batch_sz:
            img_batch.append(frame)
        else:
            antt_img_batch = model(img_batch)
            queue.put(antt_img_batch)
            img_batch = [frame]
