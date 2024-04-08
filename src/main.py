from multiprocessing import JoinableQueue, Process
from annotator import antt_process
from streamer import strm_process


if __name__ == "__main__":
    image_queue = JoinableQueue()

    producer = Process(target=antt_process, args=(image_queue,))
    consumer = Process(target=strm_process, args=(image_queue,))

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()
