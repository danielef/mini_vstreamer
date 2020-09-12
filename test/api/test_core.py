from mini_vstreamer.core.config import ConfigIO, Configurable
from mini_vstreamer.core.thread import Runnable

import logging
import time

class MyCustomConfigurable(Configurable):

    '''
    Example
    '''
    def __init__(self, index, configio, system, top):
        super().__init__(index, configio, system, top)

    def set(self, key, value):
        if key == 'one':
            logging.warn('Unsupported set of key: {}'.format(key))
        else:
            super().set(key, value)


class MyRunnable(Runnable):

    '''
    Example
    '''
    def __init__(self):
        super().__init__('runnable')
        self.__count__ = 1

    def run(self):
        while self.__running__:
            logging.info('Running and sleeping {} seconds'.format(self.__count__))
            time.sleep(self.__count__)
            self.__count__ += 1


def test_configio():
    d = {'cameras': [{'name': 'default', 'videoURL': 0, 'defaultFPS': 2, 'qOut': 'frames'}],
         'queues': [{'depth': 120, 'name': 'frames'}],
         '__path__': './test/config-test.yml'}
    c = ConfigIO('./test/config-test.yml')

    #if c['queues'][0].get('depth') == 100:
    #     c['queues'][0]['depth'] = 120

    assert c.__dict__ == d
    e = MyCustomConfigurable(0, c, {}, 'queues')
    e.__ommitCheckQIn__ = True
    e.__ommitCheckQOut__ = True
    e.set('depth', 100)
    assert e.get('depth') == 100
    e.set('depth', 120)
    assert e.get('depth') == 120


def test_runnable():
    r = MyRunnable()
