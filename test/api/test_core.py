from mini_vstreamer.core.config import ConfigIO, Configurable


class MyConfigurable(Configurable):

    '''
    Example
    '''
    def __init__(self, index, configio, system):
        super().__init__(index, configio, system, 'config')

    def set(self, key, value):
        if key == 'one':
            log.warn('Unsupported set of key: {}'.format(key))
        else:
            super().set(key, value)


def test_configio():
    d = {'config': [{'item': 1, 'value': 'val1'}, {'item': 2, 'value': 'val2', 'cfg': [{'foo': 'bar'}]}], '__path__': './test/config-test.yml'}
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
