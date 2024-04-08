import cv2 as cv
from multiprocessing import JoinableQueue
import yaml
from ...my_object import MyObject

with open("./config.yaml") as handler:
    config = yaml.load(handler, yaml.FullLoader)


def process_job(
    queue: JoinableQueue,
    batch_sz: int = 1,
    video_strm: str = config["source_stream"]["url"],
) -> None:
    model = MyObject("bar")
    capture = cv.VideoCapture(video_strm)
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
