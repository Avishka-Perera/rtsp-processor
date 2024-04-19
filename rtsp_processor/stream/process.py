from multiprocessing import JoinableQueue
from typing import Dict
from ..util import make_obj_from_conf
import cv2


def process_job(image_queue: JoinableQueue, config: Dict) -> None:
    source_url = config["source_stream"]["url"]
    batch_size = config["processor"]["batch_size"]
    processor_conf = config["processor"]
    processor = make_obj_from_conf(processor_conf)
    capture = cv2.VideoCapture(source_url)
    img_batch = []
    while True:
        grabbed, frame = capture.read()
        if not grabbed:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # bgr -> rgb

        img_batch.append(frame)
        if len(img_batch) >= batch_size:
            proc_batch = processor(img_batch)
            image_queue.put(proc_batch)
            img_batch = []
