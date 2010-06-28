package ob.android.model;

public class OrientationImpl 
implements Orientation
{
    private Double azimuth;
    
    private Double pitch;
    
    private Double roll;

    public Double getAzimuth()
    {
        return azimuth;
    }

    public void setAzimuth(Double azimuth)
    {
        this.azimuth = azimuth;
    }

    public Double getPitch()
    {
        return pitch;
    }

    public void setPitch(Double pitch)
    {
        this.pitch = pitch;
    }

    public Double getRoll()
    {
        return roll;
    }

    public void setRoll(Double roll)
    {
        this.roll = roll;
    }
}
