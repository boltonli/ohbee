import java.util.Date;

import javax.microedition.location.Location;

public class LocationUpdatedEvent
{
	private final Location location;
	
	private final Date date;
	
	public LocationUpdatedEvent(Location location)
	{
		this.location = location;
		date = new Date();
	}
	
	public Location getLocation()
	{
		return location;
	}
	
	public Date getTime()
	{
		return date;
	}
}
