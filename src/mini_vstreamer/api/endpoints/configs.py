from flask import Response
from flask_restx import fields, Resource
from mini_vstreamer.api.defaults import api, system
import cv2

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
            system['cameras'][name][field] = config_model[field].format(value)
            return system['cameras'][name]
        else:
            return 'Camera \'{}\' not found'.format(name), 404


@ns_plural.route('/')
class CameraItems(Resource):

    def get(self):
        return system['cameras']

def encode(name):
    while True:
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        result, img_encoded = cv2.imencode('.jpg', system['video'][name], encode_param)
        contents = img_encoded.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + contents + b'\r\n')

@ns.route('/<string:name>/video')
class CameraVideo(Resource):

    def get(self, name):
        return Response(encode(name), mimetype='multipart/x-mixed-replace; boundary=frame')
