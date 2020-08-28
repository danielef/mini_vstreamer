import json

from mini_vstreamer.app import initialize_app
from flask import Flask

app = Flask(__name__)
initialize_app(app)
client = app.test_client()


def test_base():
    url = '/'
    response = client.get(url)

    assert response.get_data().decode('utf-8') == 'ok'
    assert response.status_code == 200
    
def test_not_found():
    url = '/not_found'
    response = client.get(url)

    assert response.get_data().decode('utf-8') == 'ok'
    assert response.status_code == 500
