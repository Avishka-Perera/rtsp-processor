import cv2 as cv


class MyProcessor:
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
