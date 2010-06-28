import java.util.Enumeration;
import java.util.Vector;

import javax.microedition.location.Criteria;
import javax.microedition.location.Location;
import javax.microedition.location.LocationListener;
import javax.microedition.location.LocationProvider;

public class LocationListenerService
extends ServiceThread
implements LocationListener
{
	private final Object syncObject = new Object();
	
	private final Vector listeners = new Vector();
	
	private Location location;
	
	public LocationListenerService(UncaughtExceptionHandler handler)
	{
		super(handler);
	}
	
	public void locationUpdated(LocationProvider provider, Location location)
	{
		synchronized(syncObject) 
		{
			this.location = location;
			syncObject.notifyAll();
		}
	}

	public void providerStateChanged(LocationProvider provider, int state)
	{
		
	}
	
	public void addLocationUpdatedListener(LocationUpdatedListener listener)
	{
		if(!listeners.contains(listener))
			listeners.addElement(listener);
	}
	
	public void removeLocationUpdatedListener(LocationUpdatedListener listener)
	{
		listeners.removeElement(listener);
	}

	protected void runInternal()
	throws Exception
	{
		Configuration config = ConfigurationDAO.loadConfiguration();
		LocationProvider provider = LocationProvider.getInstance(new Criteria());
		provider.setLocationListener(this, 
				config.getProviderInterval(), 
				config.getProviderTimeout(),
				config.getProviderMaxAge());
		Location location;		
		while(true)
		{
			synchronized(syncObject)
			{
				syncObject.wait();
				location = this.location;
			}
			notifyListers(location);
		}
	}
	
	private void notifyListers(Location location)
	{
		LocationUpdatedEvent event = new LocationUpdatedEvent(location);
		for(Enumeration e = listeners.elements(); e.hasMoreElements(); )
			((LocationUpdatedListener)e.nextElement()).locationupdated(event);
	}
}
