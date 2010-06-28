import javax.microedition.rms.RecordStore;

public class ConfigurationDAO 
{
	private static final String RECORD_STORE_NAME = "configuration";
	
	public static synchronized Configuration loadConfiguration()
	throws Exception
	{
		RecordStore store = RecordStore.openRecordStore(RECORD_STORE_NAME, true);
		Configuration configuration = new Configuration();
		configuration.setDeviceID(new String(store.getRecord(
				Configuration.DEVICEID)));
		configuration.setProviderInterval(Integer.parseInt(
				new String(store.getRecord(Configuration.PROVIDERINTERVAL))));
		configuration.setProviderMaxAge(Integer.parseInt(
				new String(store.getRecord(Configuration.PROVIDERMAXAGE))));
		configuration.setProviderTimeout(Integer.parseInt(
				new String(store.getRecord(Configuration.PROVIDERTIMEOUT))));
		configuration.setUploadURL(new String(store.getRecord(
				Configuration.PROVIDERUPLOADURL)));
		store.closeRecordStore();
		return configuration;
	}
	
	public static synchronized void saveConfiguration(Configuration configuration)
	throws Exception
	{
		try
		{
			RecordStore.deleteRecordStore(RECORD_STORE_NAME);
		}
		catch(Exception e){}
		RecordStore store = RecordStore.openRecordStore(RECORD_STORE_NAME, true);
		byte[] data = configuration.getDeviceID().getBytes();
		store.addRecord(data, 0, data.length);
		data = String.valueOf(configuration.getProviderInterval()).getBytes();
		store.addRecord(data, 0, data.length);
		data = String.valueOf(configuration.getProviderMaxAge()).getBytes();
		store.addRecord(data, 0, data.length);
		data = String.valueOf(configuration.getProviderTimeout()).getBytes();
		store.addRecord(data, 0, data.length);
		data = configuration.getUploadURL().getBytes();
		store.addRecord(data, 0, data.length);
		store.closeRecordStore();
	} 
}
