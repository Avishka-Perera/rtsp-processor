from multiprocessing import JoinableQueue
import subprocess
import queue
import cv2
import yaml

with open("./config.yaml") as handler:
    config = yaml.load(handler, yaml.FullLoader)

sz = config["source_stream"]["size"]
width, height = sz["width"], sz["height"]
fps = config["source_stream"]["fps"]
rtsp_server_address = (
    f"rtsp://localhost:{config['sink_stream']['port']}/{config['sink_stream']['path']}"
)


def stream_job(image_queue: JoinableQueue):
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
        rtsp_server_address,
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
