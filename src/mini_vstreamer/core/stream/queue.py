from mini_vstreamer.api.defaults import system
from mini_vstreamer.core.config import Configurable
from queue import Queue as Q

import logging


class Queue(Configurable, Q):

    def __init__(self, index, configio):
        Configurable.__init__(self, index, configio, None, 'queues')
        Q.__init__(self, self.get('depth'))
        logging.debug("index: {}, name: {}".format(index, self.__configio__['queues'][index]['name']))

    def get(self, key=None, default=None):
        if key is None and default is None:
            return Queue.get(self)
        else:
            return Configurable.get(self, key, default)


def mutate_system(config):
    system['queues'] = {}
    for index, config_element in enumerate(config['queues']):
        queue_name = config_element['name']
        system['queues'][queue_name] = Queue(index, config)
