import logging
from threading import Thread
from flask import Blueprint
from mini_vstreamer.api.defaults import app, api, system
from mini_vstreamer.api.endpoints.configs import ns as config_ns
from mini_vstreamer.core.config import ConfigIO
from mini_vstreamer.core.stream.queue import mutate_system as load_queues
from mini_vstreamer.core.stream.camera import mutate_system as load_cameras

def setup(flask_app):
    flask_app.config['SERVER_NAME'] = '0.0.0.0:8888'
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
    flask_app.config['RESTPLUS_VALIDATE'] = True
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = False
    #flask_app.config['ERROR_404_HELP'] = 

def initialize_app(flask_app):
    setup(flask_app)
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)

    @flask_app.route('/foo')
    def foo():
        return 'foo'
    api.add_namespace(config_ns)
    #api.add_namespace(blog_categories_namespace)
    flask_app.register_blueprint(blueprint)

    #db.init_app(flask_app

def independent_collector():
    while True:
        if  system['queues']['frames'] is None:
            print('queue is None')

        camera_name, frame = system['queues']['frames'].get()
        system['video'][camera_name] = frame
        system['queues']['frames'].task_done()

def main():
    initialize_app(app)
    logging.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    config = ConfigIO('./config.yaml')
    load_queues(config)
    load_cameras(config)

    c_thread = Thread(name='Collector' ,target=independent_collector, args=())
    c_thread.daemon=True
    c_thread.start()

    app.run(host='0.0.0.0', threaded=True)

if __name__ == '__main__':
    main()
