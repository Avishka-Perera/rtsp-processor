import numpy as np
from typing import Sequence
import subprocess
import cv2
from time import time


class Streamer:
    def __init__(
        self, url: str, fps: int, size_hw: Sequence[int], backend: str = "opencv"
    ) -> None:
        assert backend in ["opencv", "ffmpeg"]
        self.published_count = 0
        self.url = url
        self.backend = backend
        self.wh = size_hw[::-1]
        height, width = size_hw
        if backend == "ffmpeg":
            ffmpeg_cmd = [
                "ffmpeg",
                "-re",
                "-f",
                "rawvideo",
                "-pix_fmt",
                "rgb24",
                "-s",
                f"{width}x{height}",
                "-i",
                "-",
                "-r",
                str(fps),
                "-c:v",
                "libx264",
                "-f",
                "rtsp",
                url,
            ]
            self.ffmpeg_process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
        else:
            cv2_out = cv2.VideoWriter(
                "appsrc ! videoconvert"
                + " ! video/x-raw,format=I420"
                + " ! x264enc speed-preset=ultrafast bitrate=600 key-int-max="
                + str(fps * 2)
                + " ! video/x-h264,profile=baseline"
                + f" ! rtspclientsink location={url}",
                cv2.CAP_GSTREAMER,
                0,
                fps,
                (width, height),
                True,
            )
            if not cv2_out.isOpened():
                raise Exception("can't open video writer")
            self.cv2_out = cv2_out
        self.start = time()

    def __call__(self, img_batch: Sequence[np.ndarray]) -> None:
        for img in img_batch:
            img = cv2.resize(img, self.wh)
            img = img.astype(np.uint8)
            if self.backend == "ffmpeg":
                image_bytes = img.tobytes()
                self.ffmpeg_process.stdin.write(image_bytes)
                self.ffmpeg_process.stdin.flush()
            else:
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # rgb -> bgr
                self.cv2_out.write(img)

        self.published_count += len(img_batch)
        if self.backend == "opencv":
            now = time()
            print(
                f"\rframe: {self.published_count}       fps: {self.published_count/(now-self.start)}",
                end="",
            )

    def close(self) -> None:
        if self.backend == "ffmpeg":
            self.ffmpeg_process.stdin.close()
            self.ffmpeg_process.wait()
        else:
            self.cv2_out.release()
