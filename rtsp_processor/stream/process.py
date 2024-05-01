from multiprocessing import JoinableQueue
from typing import Dict
from ..util import make_obj_from_conf, AspectSaveResize
import cv2


def process_job(image_queue: JoinableQueue, config: Dict) -> None:
    source_url = config["source_stream"]["url"]
    batch_size = config["processor"]["batch_size"]
    processor_conf = config["processor"]
    input_hw = config["source_stream"]["input_hw"]
    process_hw = config["source_stream"]["process_hw"]
    processor = make_obj_from_conf(processor_conf)
    capture = cv2.VideoCapture(source_url)
    trans = AspectSaveResize(inp_shape=input_hw, out_shape=process_hw)
    img_batch = []
    while True:
        grabbed, frame = capture.read()
        if not grabbed:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # bgr -> rgb
        frame = trans(frame)

        img_batch.append(frame)
        if len(img_batch) >= batch_size:
            proc_batch = processor(img_batch)
            image_queue.put(proc_batch)
            img_batch = []
