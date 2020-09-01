import logging

from flask import Blueprint
from mini_vstreamer.api.defaults import app, api, system
from mini_vstreamer.api.endpoints.configs import ns as config_ns

def setup(flask_app):
    flask_app.config['SERVER_NAME'] = 'localhost:8888'
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

def initialize_system(system):
    system['cameras'] = {}
    system['cameras']['default'] ={
        'id': 0,
        'name': 'default',
        'fps': 0,
        'width': 0,
        'height': 0
    }

def main():
    initialize_system(system)
    initialize_app(app)
    logging.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=True)

if __name__ == '__main__':
    main()
