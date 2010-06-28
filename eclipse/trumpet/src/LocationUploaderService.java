import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

import javax.microedition.io.Connector;
import javax.microedition.io.HttpConnection;
import javax.microedition.location.Location;

public class LocationUploaderService
extends ServiceThread
implements LocationUpdatedListener
{
	private final Object syncObject = new Object();
	
	private final LocationJSONSerializer serializer = new LocationJSONSerializer();
	
	private Location location;
	
	public LocationUploaderService(UncaughtExceptionHandler exceptionHandler)
	{
		super(exceptionHandler);
	}
	
	public void locationupdated(LocationUpdatedEvent event) 
	{
		synchronized(syncObject) 
		{
			location = event.getLocation();
			syncObject.notifyAll();
		}
	}

	protected void runInternal() 
	throws InterruptedException 
	{		
		while(true)
		{
			synchronized(syncObject)
			{
				syncObject.wait();			
			}
			uploadLocation(location);
		}
	}
	
	private void uploadLocation(Location location)
	{
		try
		{
			//TODO Get variables from configuration
			HttpConnection connection = null;
			OutputStream out = null;
			InputStream in = null;
			try 
	        {
				connection = (HttpConnection)Connector.open(
						"http://www.mrl.nott.ac.uk/~djp/location.php");
				connection.setRequestMethod(HttpConnection.POST);
				connection.setRequestProperty(
						"Content-Type", "application/json; charset=UTF-8");
				out = connection.openOutputStream();
				byte[] data = serializer.serialize(location).getBytes("UTF-8");
				out.flush();
				out.write(data);
				int responseCode = connection.getResponseCode();
	            if(responseCode != HttpConnection.HTTP_OK)
	                throw new IOException(
	                		"Server did not return response HTTP_OK (Response code was " 
	                		+ responseCode + ")");
	        } 
	        finally 
	        {
	            if(out != null)
	               out.close();
	            if(in != null)
	            	in.close();
	            if(connection != null)
	                connection.close();
	        }
		}
		catch(Exception e)
		{
			Trumpet.getMidletInstance().handleException(e);
		}
	}
}
