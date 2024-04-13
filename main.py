from multiprocessing import JoinableQueue, Process
from src.util.stream.processor import process_job
from src.util.stream.streamer import stream_job
import yaml


if __name__ == "__main__":

    with open("./config.yaml") as handler:
        config = yaml.load(handler, yaml.FullLoader)

    image_queue = JoinableQueue()

    producer = Process(target=process_job, args=(image_queue, config))
    consumer = Process(target=stream_job, args=(image_queue, config))

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()
