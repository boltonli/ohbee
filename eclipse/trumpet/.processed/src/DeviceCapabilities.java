
public class DeviceCapabilities 
{	
	public static boolean isJSR179Enabled()
	{
		try
		{
			Class.forName("javax.microedition.location.LocationProvider");
			return true;
		}
		catch(ClassNotFoundException e)
		{
			return false;
		}
	}
}
