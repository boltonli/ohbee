import httplib
import logging
import traceback
import urllib

from misc import Config
from simplejson import simplejson

class RemoteAPI(object):
        
    DEFAULT_HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}
        
    def __init__(self):
        self.jsonParser = simplejson()
        
    def connect(self):
        self.connection = httplib.HTTPConnection(\
                Config.remoteAPIHost,\
                Config.remoteAPIPort)
        self.connection.connect()
    
    def disconnect(self):
        self.connection.close()
        self.connection = None
        
    def reconnect(self):
        try:
            self.disconnect()
            self.connect()
        except:
            pass
        
    def postMobileUpload(self, data):
        response = None
        try:
            encoded = urllib.urlencode({"upload": data})
            self.connection.request("POST",\
                                    Config.mobileUploadURL,\
                                    encoded,\
                                    RemoteAPI.DEFAULT_HEADERS)
            response = self.connection.getresponse()
            response.read()
            return response.status
        except:
            logging.error(traceback.format_exc())
            if response:
                return response.status
            else:
                self.reconnect()
                return 0
    
    def getMobileList(self):
        self.connection.request("GET", Config.mobileListURL)
        response = self.connection.getresponse()
        if response.status == httplib.OK:
            return self.jsonParser.loads(response.read())
        else:
            return None
