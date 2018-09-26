import copy
import logging
import threading
import time

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
)


class Thread(object):
    def __init__(
            self,
            thread_object,
            threads_args
    ):
        self.thread_object = thread_object
        self.threads_args = threads_args

    def __repr__(self):
        return "Name: {} Args: {}".format(self.thread_object.name, self.threads_args)


class ThreadProcessor(object):
    """
    Generate tasks for each argument in a list and
    execute them on a fixed number of threads
    """

    def __init__(
            self,
            thread_func,
            thread_func_args_list,
            max_threads
    ):
        """
        :param thread_func: function to execute in each thread
        :param thread_func_args_list: arguments passed to thread_func
        :param max_threads: max number of threads to spawn
        """
        self.thread_func = thread_func
        self.thread_func_args_list = copy.deepcopy(thread_func_args_list)
        self.max_threads = max_threads

    def start(self):
        threads = list()
        thread_counter = -1
        create_threads = True
        monitor_threads = True
        while create_threads or monitor_threads:
            if create_threads and len(self._fetch_active_threads(threads)) < self.max_threads:
                thread_counter += 1
                thread = self._create_thread(thread_name=thread_counter)
                if thread:
                    threads.append(thread)
                    monitor_threads = True
                    continue
                else:
                    logging.info("No more threads to create")
                    create_threads = False
            if monitor_threads:
                active_threads = self._fetch_active_threads(threads)
                if not active_threads:
                    monitor_threads = False
                else:
                    logging.info("{} active threads".format(active_threads))
                    time.sleep(10)
        logging.info("All threads complete")
        logging.info("Bye")

    @staticmethod
    def _fetch_active_threads(threads):
        active_threads = list()
        for thread in threads:
            if thread.thread_object.is_alive():
                active_threads.append(thread)
        return active_threads

    def _create_thread(self, thread_name):
        if len(self.thread_func_args_list) > 0:
            thread_args = self.thread_func_args_list.pop()
            t = threading.Thread(
                name=thread_name,
                target=self.thread_func,
                args=thread_args
            )
            t.setDaemon(True)
            t.start()
            thread = Thread(thread_object=t, threads_args=thread_args)
            logging.info("Started Thread {}".format(thread))
            return thread
