import positioning
import sensor

class Position(object):
        
    def __init__(self, moduleID = positioning.default_module()):
        self.callbacks = []
        positioning.select_module(moduleID)
        positioning.set_requestors([{"type":"service", \
                                     "format":"application", \
                                     "data":"test_app"}])
    
    def startListening(self):
        positioning.position(course = 1, satellites = 1, callback = self.dataChanged)
    
    def stopListening(self):
        positioning.stop_position()
    
    def dataChanged(self, pos):
        for callback in self.callbacks:
            callback(pos)


class Sensors(object):
    
    def __init__(self):
        self.sensors = []
        self.callbacks = []
        module = __import__("sensor")
        for channel in sensor.list_channels():
            try:
                sen = getattr(module, channel["name"])()
                sen.set_callback((lambda x=sen: self.dataChanged(x)))
                self.sensors.append(sen)
                sen.channelName = channel["name"]
            except AttributeError,e:
                pass
            except TypeError, e:
                pass
    
    def startListening(self):
        for sen in self.sensors:
            sen.start_listening()
    
    def stopListening(self):
        for sen in self.sensors:
            sen.stop_listening()
    
    def dataChanged(self, sen):
        for callback in self.callbacks:
            callback(sen)
