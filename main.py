from multiprocessing import JoinableQueue, Process
from src.util.stream.processor import process_job
from src.util.stream.streamer import stream_job


if __name__ == "__main__":
    image_queue = JoinableQueue()

    producer = Process(target=process_job, args=(image_queue,))
    consumer = Process(target=stream_job, args=(image_queue,))

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()
