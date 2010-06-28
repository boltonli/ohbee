import sys
sys.path[0] = "e:\\Python"

import api
import logging
import sensors
import time
import threading
import httplib
import ui

from misc import *
from serialization import Serializer

init()
    
def report(sens, responseCode):
    print ""
    print "========================="
    print "Time: %s" % (time.asctime())
    if "position" in sens:
        print "Vertical accuracy: %f" % (sens["position"]["vertical_accuracy"])
        print "Horizontal accuracy: %f" % (sens["position"]["horizontal_accuracy"])
    else:
        print "GPS: No location"
    success = "Upload succeeded"
    if responseCode != httplib.OK:
        success = "Upload failed" 
    print "Response code: %d (%s)" % (responseCode, success)
    print ""

readings = {}
nexttime = time.clock() + 10
lock = threading.RLock()
rpcapi = api.RemoteAPI()
rpcapi.connect()
deviceID = ui.selectDevice(rpcapi)
allowedAttributes = ["ambient_light", "proximity_state", \
                     "device_orientation", "azimuth", "x", \
                     "y", "z", "direction"]
serizer = Serializer()
def sensorCallback(sens):
    global nexttime, readings, allowedAttributes, lock, connection, serizer, deviceID, rpcapi
    lock.acquire()
    if hasattr(sens, "channelName"):
        r = {}
        for attr in dir(sens):
            if attr in allowedAttributes:
                r[attr] = getattr(sens, attr)
        readings[sens.channelName] = r
        #logging.debug("%s: %s" % (sens.channelName, str(r)))
    elif isinstance(sens, dict):
        if "position" in sens:
            readings["position"] = sens["position"]
            readings["position"]["time"] = sens["satellites"]["time"]
            readings["position"]["heading"] = sens["course"]["heading"]
    if time.clock() < nexttime:
        lock.release()
        return
    nexttime = time.clock() + 10
    serd = serizer.serialize(readings, deviceID)
    logging.debug(serd)
    status = rpcapi.postMobileUpload(serd)
    report(readings, status)
    lock.release()
        
position = sensors.Position()
position.callbacks.append(sensorCallback)
position.startListening()
#sensor = sensors.Sensors()
#sensor.callbacks.append(sensorCallback)
#sensor.startListening()
