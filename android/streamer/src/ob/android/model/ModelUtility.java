package ob.android.model;

public class ModelUtility
{
    public void updateOrientation(Double azimuth, Double pitch, Double roll, Model model)
    {
        OrientationImpl orientation = new OrientationImpl();
        orientation.setAzimuth(azimuth);
        orientation.setPitch(pitch);
        orientation.setRoll(roll);
        model.setOrientation(orientation);
    }
    
    public void updateLocation(android.location.Location location, Model model)
    {
        LocationImpl newLocation = new LocationImpl();
        if(location.hasAccuracy())
            newLocation.setAccuracy(new Double(location.getAccuracy()));
        if(location.hasAltitude())
            newLocation.setAltitude(new Double(location.getAltitude()));
        if(location.hasBearing())
            newLocation.setBearing(new Double(location.getBearing()));
        newLocation.setLatitude(new Double(location.getLatitude()));
        newLocation.setLongitude(new Double(location.getLongitude()));
        if(location.hasSpeed())
            newLocation.setSpeed(new Double(location.getSpeed()));
        model.setLocation(newLocation);
    }
}
