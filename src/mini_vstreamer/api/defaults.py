import logging

from flask_restx import Api

api = Api(version='0.1', 
          title='mini-vstreamer',
          description='Mini Video Streamer via HTTP')

@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    print('message: {}'.format(message))
    logging.exception(message)
    return {'message': message}, 500
