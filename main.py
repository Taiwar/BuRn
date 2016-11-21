import threading
from queue import Queue
from spider import Spider
from general import *

WORKING_DIRECTORY_NAME = 'sets'
BASE_DIR = ''
QUEUE_FILE = WORKING_DIRECTORY_NAME + '/queue.txt'
CRAWLED_FILE = WORKING_DIRECTORY_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 4
REGULAR_EXPRESSION = r''
REPLACER_STRING = ''
queue = Queue()

Spider(WORKING_DIRECTORY_NAME, BASE_DIR, REGULAR_EXPRESSION, REPLACER_STRING)


# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        dir_uri = queue.get()
        Spider.crawl_dir(threading.current_thread().name, dir_uri)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_dirs = file_to_set(QUEUE_FILE)
    if len(queued_dirs) > 0:
        print(str(len(queued_dirs)) + ' dirs in the queue')
        create_jobs()
    else:
        delete_file_contents(CRAWLED_FILE)
        print("Finished!")


create_workers()
crawl()
