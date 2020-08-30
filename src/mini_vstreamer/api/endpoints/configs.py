from flask_restx import fields, Resource
from mini_vstreamer.api.defaults import api, system

ns = api.namespace('config', description='Config camera parameters')

config = api.model('Camera config', { 'id' : fields.Integer(description=''), 
                                      'name' : fields.String(description=''),
                                      'fps' : fields.Integer(description=''),
                                      'width' : fields.Integer(description=''),
                                      'height' : fields.Integer(description='')})


@ns.route('/<string:name>')
class ConfigItem(Resource):
    
    @api.marshal_with(config)
    def get(self, name):
        return system['cameras'][name]
