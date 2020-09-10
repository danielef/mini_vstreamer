from collections.abc import MutableMapping
from mini_vstreamer.core.utils import read_yml_file

import os
import yaml


class ConfigIO(MutableMapping):

    '''
    Mapping that works like a dict with storage in path
    '''
    def __init__(self, path, *args, **kwargs):
        self.__dict__.update(*args, **kwargs)
        self.__path__ = path

        if os.path.isfile(path):
            if len(args) == 0 and not bool(kwargs):
                self.__dict__ = read_yml_file(path)
                self.__path__ = path
            else:
                raise Exception('File \'{}\' already exists.'.format(path))
        else:
            self.__write()

    def __data_cleaner(self):
        '''Returns internal dict without metadata'''
        data = self.__dict__.copy()
        data.pop('__path__')
        return data

    def __write(self):
        '''Writes internal dict content to path'''
        with open(self.__path__, 'w') as yaml_file:
            data = self.__data_cleaner()
            yaml.dump(data, yaml_file, default_flow_style=False)

    def __setitem__(self, key, value):
        '''Sets an item and writes internal dict in path'''
        self.__dict__[key] = value
        self.__write()

    def __getitem__(self, key):
        '''Gets an item from internal memory dict '''
        return self.__dict__[key]

    def __delitem__(self, key):
        '''Deletes an item and writes internal dict in path'''
        del self.__dict__[key]
        self.__write()

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        '''returns simple dict representation of the mapping'''
        return str(self.__dict__)

    def __repr__(self):
        '''echoes class, id, & reproducible representation in the REPL'''
        return '{}, ConfigIO({})'.format(super(ConfigIO, self).__repr__(), self.__dict__)

    def getPath(self):
        return self.__path__


class Configurable:

    '''
    Contract and generic methods of a YAML configurable item
    '''
    def __init__(self, index, configio, system=None, configContext=None):
        self.__index__ = index
        self.__configio__ = configio
        self.__system__ = system
        self.__configContext__ = configContext
        self.__ommitCheckQIn__ = False
        self.__ommitCheckQOut__ = False

    def get(self, key=None, default=None):
        return self.__configio__[self.__configContext__][self.__index__].get( key, default)

    def set(self, key, value):
        context = self.__configContext__
        configio_copy = self.__configio__[context].copy()
        configio_copy[self.__index__][key] = value
        self.__configio__[context] = configio_copy

    def delete(self, key):
        context = self.__configContext__
        configio_copy = self.__configio__[context].copy()
        del configio_copy[self.__index__][key]
        self.__configio__[context] = configio_copy

    def configSlice(self):
        return self.__configio__[self.__configContext__][self.__index__]

    def setQueues(self):
        if not get_with_default(self.__system__, 'queues', False):
            return log.error('system without queues initialized')
        in_queue_name = self.get('qIn', None)
        out_queue_name = self.get('qOut', None)
        context = self.__configContext__
        name = self.get('name')

        if self.__ommitCheckQIn__ == False:
            if in_queue_name is None:
                log.warn("Not found value for configio[\'{}\'][\'{}\'][\'qIn\']".format(context, name))
            else:
                in_queue = self.__system__['queues'].get(in_queue_name, None)
                if in_queue is None:
                    log.error("Not found queue in system[\'queues\'][\'{}\']".format(in_queue_name))
                    log.error("configio[\'{}\'][\'{}\'][\'qIn\'] = \'{}\'".format(context, name, in_queue_name))
                else:
                    self.__inQ__ = in_queue

        if self.__ommitCheckQOut__ == False:
            if out_queue_name is None:
                log.warn("Not found value for configio[\'{}\'][\'{}\'][\'qOut\']".format(context, name))
            else:
                out_queue = self.__system__['queues'].get(out_queue_name, None)
                if out_queue is None:
                    log.error("Not found queue in system[\'queues\'][\'{}\']".format(out_queue_name))
                    log.error("configio[\'{}\'][\'{}\'][\'qOut\'] = \'{}\'".format(context, name, out_queue_name))
                else:
                    self.__outQ__ = out_queue

    def withReplaceNone(self, key, replace):
        current_value = self.get(key, None)
        if current_value is None and replace is not None:
            self.set(key, replace)
