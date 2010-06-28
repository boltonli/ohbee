import appuifw
import logging
import sys
import traceback

class Config(object):
    logLevel = logging.DEBUG
    logFile = 'e:\\pungi\logs\pungi.log'
    logFormat = "%(levelname)s : %(asctime)s : %(module)s\n%(message)s"
    sensorLogInterval = 1

    remoteAPIHost = "kerouac.mrl.nott.ac.uk"
    remoteAPIPort = 80
    mobileUploadURL = "/ob/rpc/mobile_upload.html"
    mobileListURL = "/ob/rpc/mobile_list.html"
    
    uploadInterval = 10
    
def uncaughtExceptionHandler(exceptionType, exceptionObject, exceptionTraceback):
    appuifw.note(traceback.format_exc(), 'error')
    sys.exit(-1)

def init():
    logging.basicConfig(filename = Config.logFile, \
                        level = Config.logLevel, \
                        format = Config.logFormat)
    #sys.excepthook = uncaughtExceptionHandler
    