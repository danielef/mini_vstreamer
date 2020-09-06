import logging

from flask import Flask
from flask_restx import Api

app = Flask(__name__)

api = Api(version='0.1', 
          title='mini-vstreamer',
          description='Mini Video Streamer via HTTP')

system = {}

@app.route('/')
def base():
    return {'mini_vstreamer': 0.1, 'docs': '/api'}

@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    print('message: {}'.format(message))
    logging.exception(message)
    return {'message': message}, 500
