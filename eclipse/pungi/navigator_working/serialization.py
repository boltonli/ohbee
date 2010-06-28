import time

class Serializer(object):
    
    def serialize(self, s, deviceID = "Unknown"):
        now = "%i" % (int(time.time() * 1000))
        serialized = []
        serialized.append("{\"_classname\":\"ob.webapp.rpc.MobileUpload\",\"ID\":\"")
        serialized.append(deviceID)
        serialized.append("\",\"timestamp\":")
        serialized.append(now)
        serialized.append(",\"sensorData\":{\"_classname\":\"ob.webapp.rpc.SensorData\",\"orientation\":")
        
        if "OrientationData" in s:
            serialized.append(`s["OrientationData"]["device_orientation"]`)
        else:
            serialized.append("null")
        
        serialized.append(",\"azimuth\":")
        
        if "MagneticNorthData" in s:
            serialized.append(`s["MagneticNorthData"]["azimuth"]`)
        else:
            serialized.append("null")

        serialized.append(",\"doubleTapDirection\":")
        
        if "AccelerometerDoubleTappingData" in s:
            serialized.append(`s["AccelerometerDoubleTappingData"]["direction"]`)
        else:
            serialized.append("null")
            
        serialized.append(",\"magnetometerXYZ\":")
    
        if "MagnetometerXYZAxisData" in s:
            serialized.append("{\"_classname\":\"ob.webapp.rpc.XYZ\",\"x\":")
            serialized.append(`s["MagnetometerXYZAxisData"]["x"]`)
            serialized.append(",\"y\":")
            serialized.append(`s["MagnetometerXYZAxisData"]["y"]`)
            serialized.append(",\"z\":")
            serialized.append(`s["MagnetometerXYZAxisData"]["z"]`)
            serialized.append("}")
        else:
            serialized.append("null")
            
        serialized.append(",\"accelerometerXYZ\":")
        
        if "AccelerometerXYZAxisData" in s:
            serialized.append("{\"_classname\":\"ob.webapp.rpc.XYZ\",\"x\":")
            serialized.append(`s["AccelerometerXYZAxisData"]["x"]`)
            serialized.append(",\"y\":")
            serialized.append(`s["AccelerometerXYZAxisData"]["y"]`)
            serialized.append(",\"z\":")
            serialized.append(`s["AccelerometerXYZAxisData"]["z"]`)
            serialized.append("}")
        else:
            serialized.append("null")
        
        serialized.append(",\"rotationXYZ\":")
        
        if "RotationData" in s:
            serialized.append("{\"_classname\":\"ob.webapp.rpc.XYZ\",\"x\":")
            serialized.append(`s["RotationData"]["x"]`)
            serialized.append(",\"y\":")
            serialized.append(`s["RotationData"]["y"]`)
            serialized.append(",\"z\":")
            serialized.append(`s["RotationData"]["z"]`)
            serialized.append("}")
        else:
            serialized.append("null")
            
        serialized.append("},\"location\":")
        
        if "position" in s:
            serialized.append("{\"_classname\":\"ob.webapp.db.Location\",\"elevation\":")
            
            if "RotationData" in s:
                serialized.append("\"")
                serialized.append(`s["RotationData"]["x"]`)
                serialized.append("\"")
            else:
                serialized.append("null")
            
            serialized.append(",\"roll\":")
            
            if "RotationData" in s:
                serialized.append("\"")
                serialized.append(`s["RotationData"]["z"]`)
                serialized.append("\"")
            else:
                serialized.append("null")
            
            serialized.append(",\"verticalAccuracy\":")
            serialized.append(`s["position"]["vertical_accuracy"]`)
            serialized.append(",\"time\":")
            serialized.append(now)
            serialized.append(",\"latitude\":")
            serialized.append(`s["position"]["latitude"]`)
            serialized.append(",\"altitude\":")
            serialized.append(`s["position"]["altitude"]`)
            serialized.append(",\"horizontalAccuracy\":")
            serialized.append(`s["position"]["horizontal_accuracy"]`)
            serialized.append(",\"longitude\":")
            serialized.append(`s["position"]["longitude"]`)
            serialized.append(",\"heading\":")           
            
            if "heading" in s["position"] and str(s["position"]["heading"]) != "nan":
                serialized.append(`s["position"]["heading"]`)
            else:
                serialized.append("null")
            serialized.append("}")
        else:
            serialized.append("null")  
        serialized.append("}")
        
        return ''.join(serialized)
