import cv2 as cv
from multiprocessing import JoinableQueue
import yaml

with open("./config.yaml") as handler:
    config = yaml.load(handler, yaml.FullLoader)


class MyModel:
    def __init__(self, foo) -> None:
        self.foo = foo
        self.local_state = 0

    def __call__(self, img_batch):
        for im in img_batch:
            cv.putText(
                im,
                f"{self.foo} {self.local_state}",
                [20, round(im.shape[1] / 1000 * 50)],
                cv.FONT_HERSHEY_SIMPLEX,
                round(im.shape[1] / 1000 * 2),
                (255, 0, 0),
                round(im.shape[1] / 1000 * 3),
            )
            self.local_state += 1
        return img_batch


def antt_process(
    queue: JoinableQueue,
    batch_sz: int = 1,
    video_strm: str = config["source_stream"]["url"],
) -> None:
    model = MyModel("bar")
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
