import json

from mini_vstreamer.app import initialize_app
from mini_vstreamer.api.defaults import app, system
from flask import Flask

def initialize_system(system):
    system['cameras'] = {}
    system['cameras']['default'] = { 'name': 'default',
                                     'fps': 0,
                                     'width': 0,
                                     'height': 0 }

initialize_system(system)
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
    url = '/api/camera/default'
    response = client.get(url)
    assert response.json == system['cameras']['default']
    assert response.status_code == 200

def test_config_not_found():
    url = '/api/config/foo'
    response = client.get(url)
    assert response.status_code == 404
