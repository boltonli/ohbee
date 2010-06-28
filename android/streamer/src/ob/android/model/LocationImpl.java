package ob.android.model;

public class LocationImpl 
implements Location
{
    private Double accuracy;
    
    private Double altitude;
    
    private Double bearing;
    
    private Double latitude;
    
    private Double longitude;
    
    private Double speed;

    public Double getAccuracy()
    {
        return accuracy;
    }

    public void setAccuracy(Double accuracy)
    {
        this.accuracy = accuracy;
    }

    public Double getAltitude()
    {
        return altitude;
    }

    public void setAltitude(Double altitude)
    {
        this.altitude = altitude;
    }

    public Double getBearing()
    {
        return bearing;
    }

    public void setBearing(Double bearing)
    {
        this.bearing = bearing;
    }

    public Double getLatitude()
    {
        return latitude;
    }

    public void setLatitude(Double latitude)
    {
        this.latitude = latitude;
    }

    public Double getLongitude()
    {
        return longitude;
    }

    public void setLongitude(Double longitude)
    {
        this.longitude = longitude;
    }

    public Double getSpeed()
    {
        return speed;
    }

    public void setSpeed(Double speed)
    {
        this.speed = speed;
    }
}
