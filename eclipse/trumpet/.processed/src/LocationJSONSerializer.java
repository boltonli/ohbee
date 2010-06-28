import javax.microedition.location.Location;
import javax.microedition.location.LocationException;
import javax.microedition.location.Orientation;
import javax.microedition.location.QualifiedCoordinates;

public class LocationJSONSerializer 
{
	public String serialize(Location location)
	{
		if(location == null)
			return "null";
		
		StringBuffer buffer = new StringBuffer();
		buffer.append("{");
		buffer.append("\"course\":")
				.append(location.getCourse())
				.append(",");
		buffer.append("\"locationMethod\":")
				.append(location.getLocationMethod())
				.append(",");
		buffer.append("\"speed\":")
				.append(location.getSpeed())
				.append(",");
		buffer.append("\"timestamp\":")
				.append(location.getTimestamp())
				.append(",");
		buffer.append("\"isValid\":")
				.append(location.isValid())
				.append(",");
		buffer.append("\"qualifiedCoordinates\":");
		if(location.getQualifiedCoordinates() == null)
			buffer.append("null");
		else
			serialize(location.getQualifiedCoordinates(), buffer);
		buffer.append(",");
		buffer.append("\"extraInfo\":");
		serializeExtraInfo(location, buffer);
		buffer.append(",");
		buffer.append("\"orientation\":");
		serializeOrientation(buffer);
		buffer.append("}");
		
		return buffer.toString();
	}
	
	private void serialize(QualifiedCoordinates coordinates, StringBuffer buffer)
	{		
		buffer.append("{");
		buffer.append("\"altitude\":")
				.append(coordinates.getAltitude())
				.append(",");
		buffer.append("\"horizontalAccuracy\":")
				.append(coordinates.getHorizontalAccuracy())
				.append(",");
		buffer.append("\"latitude\":")
				.append(coordinates.getLatitude())
				.append(",");
		buffer.append("\"longitude\":")
				.append(coordinates.getLongitude())
				.append(",");
		buffer.append("\"verticalAccuracy\":")
				.append(coordinates.getVerticalAccuracy());
		buffer.append("}");
	}
	
	private void serializeExtraInfo(Location location, StringBuffer buffer)
	{
		buffer.append("{");
		buffer.append("\"application/X-jsr179-location-nmea\":");
		String nmea = location.getExtraInfo("application/X-jsr179-location-nmea");
		buffer.append(nmea == null ? "null" : "\"" + nmea + "\"");
		buffer.append(",");
		buffer.append("\"application/X-jsr179-location-lif\":");
		String lif = location.getExtraInfo("application/X-jsr179-location-lif");
		buffer.append(lif == null ? "null" : "\"" + lif + "\"");
		buffer.append(",");
		buffer.append("\"text/plain\":");
		String plain = location.getExtraInfo("text/plain"); 
		buffer.append(plain == null ? "null" : "\"" + plain + "\"");
		buffer.append("}");
	}
	
	private void serializeOrientation(StringBuffer buffer)
	{
		try
		{
			Orientation orientation = Orientation.getOrientation();
			if(orientation == null)
			{
				buffer.append("null");
				return;
			}
			buffer.append("{");
			buffer.append("\"compassAzimuth\":")
					.append(orientation.getCompassAzimuth())
					.append(",");
			buffer.append("\"pitch\":")
					.append(orientation.getPitch())
					.append(",");
			buffer.append("\"roll\":")
				.append(orientation.getRoll())
				.append(",");
			buffer.append("\"isOrientationMagnetic\":")
					.append(orientation.isOrientationMagnetic());
			buffer.append("}");
		} 
		catch (LocationException e) 
		{
			buffer.append("null");
		}
	}
}
