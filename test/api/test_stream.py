from mini_vstreamer.api.defaults import system
from mini_vstreamer.core.config import ConfigIO
#from mini_vstreamer.core.stream.queue import Queue
from mini_vstreamer.core.stream.queue import mutate_system as q_system

def test_queue_factory():
    c = ConfigIO('./test/config-test.yml')
    q_system(c)
    assert system['queues']['frames'].get('name') == 'frames'
    assert system['queues']['frames'].get('depth') == 120

