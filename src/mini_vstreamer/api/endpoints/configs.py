from flask_restx import fields, Resource
from mini_vstreamer.api.defaults import api, system

ns = api.namespace('config', description='Config camera parameters')
ns_plural = api.namespace('configs', description='All camera configurations')

config_model = api.model('Camera config', { 'name' : fields.String(description='Camera Name'),
                                            'fps' : fields.Integer(description='Camera Frames Per Second'),
                                            'width' : fields.Integer(description='Camera Width Pixels'),
                                            'height' : fields.Integer(description='Camera Height Pixels')})


@ns.route('/<string:name>')
class ConfigItem(Resource):
    
    @api.marshal_with(config_model)
    def get(self, name):
        if name in system['cameras']:
            return system['cameras'][name]
        else:
            return 'Camera not found', 404
            
@ns_plural.route('/')
class ConfigItems(Resource):

    def get(self):
        return system['cameras']
