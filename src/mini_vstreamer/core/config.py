import collections
import os

from mini_vstreamer import read_yml_file

class ConfigIO(collections.MutableMapping):

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
