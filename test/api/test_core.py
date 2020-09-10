from mini_vstreamer.core.config import ConfigIO, Configurable
from mini_vstreamer.core.thread import Runnable

import logging
import time

class MyConfigurable(Configurable):

    '''
    Example
    '''
    def __init__(self, index, configio, system):
        super().__init__(index, configio, system, 'config')

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
    d = {'config': [{'item': 1, 'value': 'val1'}, 
                    {'item': 2, 'value': 'val2', 'cfg': [{'foo': 'bar'}]}],
         'queues': [{'depth': 120, 'name': 'frames'}],
         '__path__': './test/config-test.yml'}
    c = ConfigIO('./test/config-test.yml')

    if c['config'][0].get('value') == 'val3':
         c['config'][0]['value'] = 'val1'

    assert c.__dict__ == d
    e = MyConfigurable(0, c, {})
    e.__ommitCheckQIn__ = True
    e.__ommitCheckQOut__ = True
    e.set('value', 'val3')
    assert c.__dict__['config'][0]['value'] == 'val3'
    e.set('value', 'val1')
    assert e.get('value') == 'val1'


def test_runnable():
    r = MyRunnable()
    assert r.status() == 'awaiting'
    r.start()
    assert r.status() == 'running'
    r.stop()
    assert r.status() == 'stopped'
