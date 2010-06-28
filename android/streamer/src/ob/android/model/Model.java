package ob.android.model;

import java.util.Observable;

public class Model
extends Observable
{
    public static enum MODEL_CHANGE_KEYS
    {
        DEVICE_ID,
        LOCATION,
        ORIENTATION;
    }
    
    private String deviceID;
    
    private Location location;
    
    private Orientation orientation;
    
    public Model(String deviceID)
    {
        this.deviceID = deviceID;
    }
    
    public String getDeviceID()
    {
        return deviceID;
    }
    
    public void setDeviceID(String deviceID)
    {
        this.deviceID = deviceID;
        setChanged();
        notifyObservers(MODEL_CHANGE_KEYS.DEVICE_ID);
    }
    
    public Location getLocation()
    {
        return location;
    }
    
    public void setLocation(Location location)
    {
        this.location = location;
        setChanged();
        notifyObservers(MODEL_CHANGE_KEYS.LOCATION);
    }
    
    public Orientation getOrientation()
    {
        return orientation;
    }
    
    public void setOrientation(Orientation orientation)
    {
        this.orientation = orientation;
        setChanged();
        notifyObservers(MODEL_CHANGE_KEYS.ORIENTATION);
    }
}
