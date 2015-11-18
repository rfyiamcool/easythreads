#coding:utf-8
from Queue import Queue,Empty
from threading import Thread, Lock, Condition
import logging

class _ThreadWorker(Thread):

    def __init__(self, tasks, on_task):
        Thread.__init__(self)
        self.daemon = True
        self.shutdown_state = False
        self.tasks = tasks
        self.on_task = on_task
        self.logger = logging.getLogger('_ThreadWorker')

    def shutdown(self):
        self.shutdown_state = True

    def run(self):
        while True:
            try:
                task = self.tasks.get(False)
                try:
                    if hasattr(task['task'], '__call__'):
                        task['task'](*task['args'])
                    else:
                        self.logger.error('Not a callable task'+str(task))
                except Exception as e:
                    task_name = "unavailable"
                    if task is not None and task['task'] is not None:
                        task_name = task['task'].__name__
                    self.logger.error('task_name = ' + task_name + ' : ' + e.message, exc_info=True)
                finally:
                    self.tasks.task_done()
            except Empty as e:
                if self.shutdown_state:
                    return
                with self.on_task:
                    self.on_task.wait()
            except Exception as e:
                self.logger.error(e.message, exc_info=True)



class AsyncWorker:

    def __init__(self, num_threads):
        self.logger = logging.getLogger('threading')
        self.tasks = Queue(0)
        self.threads = []
        self.shutdown_state = False
        self.shutdown_lock = Lock()
        self.on_task = Condition()
        for _ in range(num_threads):
            self.threads.append(_ThreadWorker(self.tasks, self.on_task))
        map(lambda thread: thread.start(), self.threads)

    def append(self, task, *kwargs):
        if not self.shutdown_state:
            self.tasks.put({'task':task, 'args': list(kwargs)})
            with self.on_task:
                #Wake up one of the thread to process task
                self.on_task.notify()
        else:
            self.logger.error('thread pool status is shutdown')

    def shutdown(self, **kwargs):
        with self.shutdown_lock:
            try:
                if not self.shutdown_state:
                    self.shutdown_state = True
                    map(lambda thread : thread.shutdown(), self.threads)
                    with self.on_task:
                        #wakeup all sleeping threads
                        self.on_task.notify_all()
                    if kwargs.get("block", True):
                        #Wait till worker threads complete
                        self.tasks.join()
                        map(lambda thread: thread.join(), self.threads)
            except Exception as e:
                self.logger.error(e.message, exc_info=True)
