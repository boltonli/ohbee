import javax.microedition.lcdui.Alert;
import javax.microedition.lcdui.AlertType;
import javax.microedition.lcdui.Command;
import javax.microedition.lcdui.CommandListener;
import javax.microedition.lcdui.Display;
import javax.microedition.lcdui.Displayable;
import javax.microedition.lcdui.Form;
import javax.microedition.lcdui.Item;
import javax.microedition.lcdui.StringItem;
import javax.microedition.lcdui.TextField;
import javax.microedition.midlet.MIDlet;
import javax.microedition.midlet.MIDletStateChangeException;

public class Trumpet
extends MIDlet
implements 	CommandListener,
			LocationUpdatedListener,
			UncaughtExceptionHandler
{		
	private static Trumpet midletInstance;
	
	private final Form mainForm = new Form("Trumpet");
	
	private final StringItem locationFormItem = new StringItem("Current Location", ""); 
	
	private final Command exitCommand = new Command("Exit", Command.EXIT, 1);
	
	private final Command configureCommand = new Command("Configure", Command.SCREEN, 2);
	
	private final Command startCommand = new Command("Start", Command.SCREEN, 3);
	
	private final Command stopCommand = new Command("Stop", Command.SCREEN, 4);
	
	private final Command saveCommand = new Command("Save", Command.OK, 2);
	
	private final Command cancelCommand = new Command("Cancel", Command.CANCEL, 3);
	
	private final LocationJSONSerializer serializer = new LocationJSONSerializer();
	
	private LocationListenerService locationListenerService;
	
	private LocationUploaderService locationUploaderService;
	
	public Trumpet()
	{
		midletInstance = this;
		mainForm.setCommandListener(this);
		mainForm.addCommand(exitCommand);
		
		if(DeviceCapabilities.isJSR179Enabled())
		{
			mainForm.append(locationFormItem);
			mainForm.addCommand(configureCommand);
			mainForm.addCommand(startCommand);
		}
		else
		{
			StringItem errorItem = new StringItem("Fatal Error", 
					"This device does not support the J2ME Location Service, " +
					"you will not be able to run this application on this device.");
			mainForm.append(errorItem);
		}		
	}

	protected synchronized void destroyApp(boolean force)
	throws MIDletStateChangeException 
	{
		try
		{
			if(locationUploaderService != null 
					&& locationUploaderService.isRunning())
				locationUploaderService.stopAndWait();
			if(locationListenerService != null 
					&& locationListenerService.isRunning())
				locationListenerService.stopAndWait();
		}
		catch(InterruptedException e)
		{
			throw new MIDletStateChangeException(e.getMessage());
		}
	}

	protected synchronized void pauseApp(){}

	protected synchronized void startApp()
	throws MIDletStateChangeException 
	{
		Display.getDisplay(this).setCurrent(mainForm);
		StringItem item = new StringItem("JSR256", "");
		try
		{
			Class.forName("javax.microedition.sensor.SensorManager");
			item.setText("Yes");
		}
		catch(Exception e)
		{
			item.setText("No");
		}
		mainForm.append(item);
	}

	public void commandAction(Command command, Displayable screen) 
	{
		if(command == exitCommand)
		{
			try 
			{
				destroyApp(true);
			}
			catch(MIDletStateChangeException e) 
			{
				handleException(e);
			}
			notifyDestroyed();
		}
		else if(command == startCommand)
			start();
		else if(command == stopCommand)
			stop();
		else if(command == configureCommand)
			configure();
		else if(command == saveCommand && screen instanceof Form)
			saveConfiguration((Form)screen);
		else if(command == cancelCommand)
			Display.getDisplay(this).setCurrent(mainForm);
	}

	public void locationupdated(LocationUpdatedEvent event)
	{
		locationFormItem.setText(serializer.serialize(event.getLocation()));
	}

	public void handleUncaughtException(UncaughtExceptionEvent event) 
	{
		handleException(event.getUncaughtException());
	}
	
	public void handleException(Exception exception)
	{
		Alert alert = new Alert("An Error Occurred", 
				"The error message was: " + exception.toString() +
				". If the error continues to occur, please exit the " +
				"application and inform an application developer",
				null, AlertType.ERROR);
		alert.setTimeout(Alert.FOREVER);
		Display.getDisplay(this).setCurrent(alert, mainForm);		
		
		//#mdebug warn
		System.out.println(exception.getMessage());
		exception.printStackTrace();
		//#enddebug
	}
	
	private void start()
	{
		if(locationListenerService == null)
			locationListenerService = new LocationListenerService(this);
		if(locationUploaderService == null)
		{
			locationUploaderService = new LocationUploaderService(this);
			locationListenerService.addLocationUpdatedListener(locationUploaderService);
			locationListenerService.addLocationUpdatedListener(this);
		}
		
		try
		{
			new Thread(locationListenerService).start();
			new Thread(locationUploaderService).start();	
		}
		catch(Exception e)
		{
			handleException(e);
		}
		
		mainForm.removeCommand(startCommand);
		mainForm.addCommand(stopCommand);
	}
	
	private void stop()
	{
		try
		{
			if(locationUploaderService != null 
					&& locationUploaderService.isRunning())
				locationUploaderService.stopAndWait();
			if(locationListenerService != null 
					&& locationListenerService.isRunning())
				locationListenerService.stopAndWait();
		}
		catch(InterruptedException e)
		{
			handleException(e);
		}
		
		mainForm.removeCommand(stopCommand);
		mainForm.addCommand(startCommand);
	}
	
	private void configure()
	{
		Form form = new Form("Configuration");
		form.addCommand(cancelCommand);
		form.addCommand(saveCommand);
		form.addCommand(exitCommand);
		form.setCommandListener(this);
		
		Configuration configuration;
		try
		{
			configuration = ConfigurationDAO.loadConfiguration();
		}
		catch(Exception e)
		{
			configuration = new Configuration();
		}
		
		TextField deviceIDField = new IdentifiableTextField(
				Configuration.DEVICEID,
				"Device ID",
				configuration.getDeviceID(), 
				30,
				TextField.ANY);
		form.append(deviceIDField);
		TextField intervalField = new IdentifiableTextField(
				Configuration.PROVIDERINTERVAL,
				"Location Interval", 
				String.valueOf(configuration.getProviderInterval()),
				10,
				TextField.NUMERIC);
		form.append(intervalField);
		TextField maxAgeField = new IdentifiableTextField(
				Configuration.PROVIDERMAXAGE,
				"Location Max Age", 
				String.valueOf(configuration.getProviderMaxAge()),
				10,
				TextField.NUMERIC);
		form.append(maxAgeField);
		TextField timeoutField = new IdentifiableTextField(
				Configuration.PROVIDERTIMEOUT,
				"Location Timeout",
				String.valueOf(configuration.getProviderTimeout()),
				10,
				TextField.NUMERIC);
		form.append(timeoutField);
		TextField uploadField = new IdentifiableTextField(
				Configuration.PROVIDERUPLOADURL,
				"Upload URL",
				configuration.getUploadURL(),
				100,
				TextField.ANY);
		form.append(uploadField);
		Display.getDisplay(this).setCurrent(form);
	}
	
	private void saveConfiguration(Form configurationForm)
	{
		Display.getDisplay(this).setCurrent(mainForm);
		Configuration configuration = new Configuration();
		int size = configurationForm.size();
		for(int i = 0; i < size; i++)
		{
			Item item = configurationForm.get(i);
			if(!(item instanceof IdentifiableTextField))
				continue;
			IdentifiableTextField configItem = (IdentifiableTextField)item;
			switch(configItem.getID())
			{
			case Configuration.DEVICEID :
				configuration.setDeviceID(configItem.getString());
				break;
			case Configuration.PROVIDERINTERVAL:
				configuration.setProviderInterval(Integer.parseInt(configItem.getString()));
				break;
			case Configuration.PROVIDERMAXAGE:
				configuration.setProviderMaxAge(Integer.parseInt(configItem.getString()));
				break;
			case Configuration.PROVIDERTIMEOUT:
				configuration.setProviderTimeout(Integer.parseInt(configItem.getString()));
				break;
			case Configuration.PROVIDERUPLOADURL:
				configuration.setUploadURL(configItem.getString());
				break;
			default :
				break;
			}
		}
		
		try
		{
			ConfigurationDAO.saveConfiguration(configuration);
		}
		catch(Exception e)
		{
			handleException(e);
		}
	}
	
	public static Trumpet getMidletInstance()
	{
		return midletInstance;
	}
}
