from multiprocessing import JoinableQueue
import subprocess
import queue
import cv2
from typing import Dict


def stream_job(image_queue: JoinableQueue, config: Dict):
    fps = str(config["fps"])
    sink_url = config["sink_stream"]["url"]
    width, height = config["sink_stream"]["size"]

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
        fps,
        "-c:v",
        "libx264",
        "-f",
        "rtsp",
        sink_url,
    ]

    process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    while True:
        try:
            image = image_queue.get(timeout=5)[0]
            if image is None:
                break

            resized_image = cv2.resize(image, (width, height))
            rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
            image_bytes = rgb_image.tobytes()

            process.stdin.write(image_bytes)
            process.stdin.flush()

            image_queue.task_done()
        except queue.Empty:
            pass

    process.stdin.close()
    process.wait()
