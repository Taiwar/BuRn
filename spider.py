from general import *
import re


class Spider:

    work_dir = ''
    base_dir = ''
    queue_file = ''
    crawled_file = ''
    regex = ''
    replace_str = ''
    queue = set()
    crawled = set()

    def __init__(self, work_dir, base_dir, regex, replace_str):
        Spider.work_dir = work_dir
        Spider.base_dir = base_dir
        Spider.queue_file = Spider.work_dir + '/queue.txt'
        Spider.crawled_file = Spider.work_dir + '/crawled.txt'
        Spider.regex = regex
        Spider.replace_str = replace_str
        self.boot()
        self.crawl_dir('First spider', Spider.base_dir)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_project_dir(Spider.work_dir)
        create_data_files(Spider.work_dir, Spider.base_dir)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_dir(thread_name, dir_uri):
        if dir_uri not in Spider.crawled:
            print(thread_name + ' now crawling ' + dir_uri)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
            Spider.add_dirs_to_queue(Spider.walk_dir(dir_uri))
            if dir_uri in Spider.queue:
                Spider.queue.remove(dir_uri)
            Spider.crawled.add(dir_uri)
            Spider.update_files()

    # Walks dir, renames files and returns directories
    @staticmethod
    def walk_dir(dir_uri):
        uris = set()
        for root, dirs, files in os.walk(dir_uri, topdown=False):
            for name in dirs:
                uris.add(name)
            for name in files:
                file_name, file_extension = os.path.splitext(name)
                regex_match = re.search(Spider.regex, file_name)
                if regex_match is not None:
                    print("Match: " + file_name)
                    new_file_name = re.sub(Spider.regex, Spider.replace_str, file_name)
                    print("New name: " + new_file_name)
                    old_file_path = os.path.join(root, name)
                    new_file_path = os.path.join(root, new_file_name + file_extension)
                    os.rename(old_file_path, new_file_path)
        return uris

    # Saves queue data to project files
    @staticmethod
    def add_dirs_to_queue(dirs):
        for dir_uri in dirs:
            if (dir_uri in Spider.queue) or (dir_uri in Spider.crawled):
                continue
            Spider.queue.add(dir_uri)

    # Updates files shared between spiders
    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
