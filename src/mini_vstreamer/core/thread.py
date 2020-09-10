from threading import Thread

import logging


class Runnable:

    def __init__(self, name):
        self.__thread_name__ = "{}-Thread".format(name)
        self.__thread__ =  None
        self.__running__ = False

    def run(self):
        raise Exception('Not implemented method run()')

    def start(self):
        logging.info('Starting {}, name: {}'.format(self.__class__, self.__thread_name__))
        if not self.__running__ and self.__thread__ is None:
            self.__thread__ = Thread(name=self.__thread_name__, target=self.run, args=(), daemon=True)
            self.__running__ = True
            self.__thread__.start()
        return self

    def stop(self):
        if self.__running__:
            logging.info('Stopping {}, name: {}'.format(self.__class__, self.__thread_name__))
            self.__running__ = False
            self.__thread__.join(1)
        return self

    def status(self):
        logging.info('Status {}, name: {}'.format(self.__class__, self.__thread_name__))
        if not self.__running__ and self.__thread__ is None:
            return 'awaiting'
        elif not self.__running__:
            return 'stopped'
        else:
            return 'running'
