import numpy as np
from typing import Sequence
import subprocess
import cv2


class Streamer:
    def __init__(
        self, url: str, fps: int, size: Sequence[int], backend: str = "opencv"
    ) -> None:
        assert backend in ["opencv", "ffmpeg"]
        self.state = 0
        self.url = url
        self.backend = backend
        self.size = size
        width, height = size
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

    def __call__(self, img: np.ndarray) -> None:
        img = img.astype(np.uint8)
        if self.backend == "ffmpeg":
            image_bytes = img.tobytes()
            self.ffmpeg_process.stdin.write(image_bytes)
            self.ffmpeg_process.stdin.flush()
        else:
            img = img[:, :, ::-1]
            self.cv2_out.write(img)
        print(f"\rframe: {self.state}", end="")
        self.state += 1

    def close(self) -> None:
        if self.backend == "ffmpeg":
            self.ffmpeg_process.stdin.close()
            self.ffmpeg_process.wait()
        else:
            self.cv2_out.release()
