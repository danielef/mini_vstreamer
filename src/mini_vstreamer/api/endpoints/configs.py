from flask_restx import fields, Resource
from mini_vstreamer.api.defaults import api, system

ns = api.namespace('camera', description='Camera parameters')
ns_plural = api.namespace('cameras', description='All camera configurations')

config_model = api.model('Camera config', { 'name' : fields.String(description='Camera Name'),
                                            'fps' : fields.Integer(description='Camera Frames Per Second'),
                                            'width' : fields.Integer(description='Camera Width Pixels'),
                                            'height' : fields.Integer(description='Camera Height Pixels')})


@ns.route('/<string:name>')
class CameraDispacher(Resource):
    
    @api.marshal_with(config_model)
    def get(self, name):
        if name in system['cameras']:
            return system['cameras'][name]
        else:
            return 'Camera not found', 404


@ns.route('/<string:name>/<string:field>/<string:value>')
class CameraUpdater(Resource):

    def put(self, name, field, value):
        if name in system['cameras']:
            print('cm: {}'.format(config_model[field].format(value)))
            system['cameras'][name][field] = value  #value automatic typing!
            return system['cameras'][name]
        else:
            return 'Camera \'{}\' not found'.format(name), 404


@ns_plural.route('/')
class CameraItems(Resource):

    def get(self):
        return system['cameras']
