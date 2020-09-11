from mini_vstreamer.api.defaults import system
from mini_vstreamer.core.config import Configurable
from mini_vstreamer.core.thread import Runnable
from threading import Thread
from time import time, sleep

import cv2
import logging
import subprocess

def open_gst_rtsp(uri, width=None, height=None, latency=2000):
    """Open an RTSP URI (IP CAM)."""
    gst_elements = str(subprocess.check_output('gst-inspect-1.0'))
    
    if 'omxh264dec' in gst_elements:
        if width is not None and height is not None:
            xraw = 'video/x-raw, width=(int){}, height=(int){}, '.format(width, height)
        elif width is not None and height is None:
            xraw = 'video/x-raw, width=(int){}, '.format(width)
        elif width is None and height is not None:
            xraw = 'video/x-raw, height=(int){}, '.format(height)
        else:
            xraw = 'video/x-raw, '
        # Uses NVDEC H.264 decoder on Jetson
        gst_str = ('rtspsrc location={} latency={} ! '
                   'rtph264depay ! h264parse ! omxh264dec ! '
                   'nvvidconv ! '
                   + xraw +
                   'format=(string)BGRx ! videoconvert ! '
                   'appsink').format(uri, latency, width, height)
    elif 'avdec_h264' in gst_elements:
        # Software decoder avdec_h264
        gst_str = ('rtspsrc location={} latency={} ! '
                   'rtph264depay ! h264parse ! avdec_h264 ! '
                   'videoconvert ! appsink').format(uri, latency)
    else:
        raise RuntimeError('H.264 decoder not found!')
    return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

class Camera(Configurable, Runnable):
    """
    Camera Object
    """

    def __init__(self, index, configio, system):
        Configurable.__init__(self, index, configio, system, 'cameras')
        Runnable.__init__(self, self.get('name'))
        self.__ommitCheckQIn__ = True
        self.__outQ__ = None
        self.__videoCapture__ = None
        self.setQueues()

    def set(self, key, value):
        Configurable.set(self, key, value)
        if key == 'qOut':
            self.setQueues()
        
    def __open(self):
        if self.__videoCapture__ is None:
            if self.get('gstEnable', False):
                self.__videoCapture__ = open_gst_rtsp(self.get('videoURL'), latency=self.get('latency', 2000))
            else:
                self.__videoCapture__ = cv2.VideoCapture(self.get('videoURL'))

            self.__measureFPS()
        else:
            logging.warn('Camera {} already opened'.format(self.get('name')))

    def __measureFPS(self):
        logging.warn('mfps: {}'.format(time()))
        if self.__videoCapture__ is None:
            logging.warn('Camera {} is not opened'.format(self.get('name')))
            return
        
        currentFPS = int(self.__videoCapture__.get(cv2.CAP_PROP_FPS))
        defaultFPS = self.get('defaultFPS', 2)
        
        if currentFPS > 120 or currentFPS <= 0:
            logging.warn('Camera {} using defaultFPS:{}, currentFPS:{} invalid'.format(self.get('name'), defaultFPS, currentFPS))
            self.__videoFPS__ = defaultFPS
        else:
            if defaultFPS != currentFPS:
                logging.warn('Camera {} using currentFPS:{}, preferred over defaultFPS:{}'.format(self.get('name'), currentFPS, defaultFPS))
            self.__videoFPS__ = currentFPS

        self.__wait__ = 1.0 / self.__videoFPS__

    def __release(self):
        try:
            self.__videoCapture__.release()
        except:
            pass
        self.__videoCapture__ = None        

    def run(self):
        self.__open()
        while self.__running__:
            sleep(self.__wait__)
            self.__videoCapture__.grab()
            _, frame = self.__videoCapture__.read()
            if frame is None:
                logging.error('Camera {} error loading frame'.format(self.get('name')))
                self.__release()
                self.__open()
                self.__measureFPS()
            else:
                self.__outQ__.put((self.get('name'), frame))
        return self


def independent_start(config):
    system['cameras']  = {}
    for index, config_element in enumerate(config['cameras']):
        camera_name = config_element['name']
        system['cameras'][camera_name] = Camera(index, config, system)
        system['cameras'][camera_name].start()

def mutate_system(config):
    if system.get('queues') is None:
        message = 'system without queues initialized, try calling stream.ymsqueues.mutate_system(system, configio_of_queues)'
        logging.error(message)
        raise Exception(message)
    else:
        c_thread = Thread(name='CameraStarter' ,target=independent_start, args=(config,))
        c_thread.daemon=True
        c_thread.start()
