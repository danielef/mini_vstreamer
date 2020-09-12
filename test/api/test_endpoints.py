import json

from mini_vstreamer.app import initialize_app
from mini_vstreamer.api.defaults import app, system
from mini_vstreamer.core.config import ConfigIO
from mini_vstreamer.core.stream.queue import mutate_system as load_queues
from mini_vstreamer.core.stream.camera import mutate_system as load_cameras

from flask import Flask

config = ConfigIO('./test/config-test.yml')
load_queues(config)
load_cameras(config)
initialize_app(app)


client = app.test_client()


def test_base():
    url = '/'
    response = client.get(url)
    
    assert response.json == {'mini_vstreamer': 0.1 , 'docs' : '/api'}
    assert response.status_code == 200
    
def test_not_found():
    url = '/not_found'
    response = client.get(url)

    assert response.get_data().decode('utf-8') != 'ok'
    assert response.status_code == 404

def test_cameras():
    url = '/api/cameras/'
    response = client.get(url)
    assert response.json == [{'name': 'default', 'videoURL': 0, 'defaultFPS': 2, 'qOut': 'frames'}]
    assert response.status_code == 200

def test_camera():
    url = '/api/camera/default'
    response = client.get(url)
    assert str(response.json) == str(system['cameras']['default'])
    assert response.status_code == 200

def test_camera_update():
    url = '/api/camera/default/defaultFPS'
    response = client.put(url, data='1')
    print('json: {}'.format(response.json))
    assert response.json['defaultFPS'] == 1
    assert response.status_code == 200

    response = client.put(url, data='2')
    assert response.json['defaultFPS'] == 2
    assert response.status_code == 200

def test_camera_state():
    url = '/api/camera/default/start'
    response = client.post(url)
    assert system['cameras']['default'].status() == 'running'
    assert response.status_code == 200

    url = '/api/camera/default/stop'
    response = client.post(url)
    assert system['cameras']['default'].status() == 'stopped'
    assert response.status_code == 200

def test_config_not_found():
    url = '/api/config/foo'
    response = client.get(url)
    assert response.status_code == 404
