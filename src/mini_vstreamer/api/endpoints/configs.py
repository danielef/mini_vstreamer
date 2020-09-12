from enum import Enum
from flask import json, request, Response
from flask_restx import fields, Resource
from mini_vstreamer.api.defaults import api, system
import cv2

ns = api.namespace('camera', description='Camera parameters')
ns_plural = api.namespace('cameras', description='All camera configurations')

config_model = api.model('Camera config', { 'name' : fields.String(description='Camera Name'),
                                            'defaultFPS' : fields.Integer(description='Camera Frames Per Second'),
                                            'qOut' : fields.Integer(description='Out Queue'),
                                            'videoURL' : fields.Raw(description='Video URL')})

def encode(name, scale):
    while True:
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        image = system['video'][name]
        if scale > 1:
            image = cv2.resize(image, (image.shape[1] // scale, image.shape[0] // scale))
        result, img_encoded = cv2.imencode('.jpg', image, encode_param)
        contents = img_encoded.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + contents + b'\r\n')


@ns.route('/<string:name>')
class CameraDispacher(Resource):
    
    def get(self, name):
        if name in system['cameras']:
            return system['cameras'][name].configSlice()
        else:
            return 'Camera not found', 404



@ns.route('/<string:name>', defaults={'state': None})
@ns.route('/<string:name>/<string:state>')
class CameraState(Resource):

    class State(str, Enum):
        start = 'start'
        stop = 'stop'

    def post(self, name, state : State):
        if name in system['cameras']:
            if state == CameraState.State.start:
                system['cameras'][name].start()
                return system['cameras'][name].status()
            elif state == CameraState.State.stop:
                system['cameras'][name].stop()
                return system['cameras'][name].status()
            else:
                return system['cameras'][name].status()
        else:
            return 'Camera not found', 404


@ns.route('/<string:name>/<string:field>')
class CameraUpdater(Resource):

    def put(self, name, field):
        value = request.data
        if name in system['cameras']:
            system['cameras'][name].set(field, config_model[field].format(value))
            return system['cameras'][name].configSlice()
        else:
            return 'Camera \'{}\' not found'.format(name), 404


@ns_plural.route('/')
class CameraItems(Resource):

    def get(self):
        system_map = next(iter(system['cameras'].values())).__configio__.__dict__
        return system_map['cameras']


@ns.route('/<string:name>/video', defaults={'scale': 1})
@ns.route('/<string:name>/video/<int:scale>')
class CameraVideo(Resource):

    def get(self, name, scale):
        return Response(encode(name, scale), mimetype='multipart/x-mixed-replace; boundary=frame')

