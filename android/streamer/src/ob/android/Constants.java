package ob.android;

import android.util.Log;

public final class Constants
{
	private static final String LOG_TAG = "streamer";
		
	public static void debug(String message)
	{
		Log.d(LOG_TAG, message);
	}
	
	public static void error(String message, Throwable error)
	{
		Log.e(LOG_TAG, message, error);
	}
	
	private Constants() { }
}
