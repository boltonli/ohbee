
public class UncaughtExceptionEvent
{
	private final Object source;
	
	private final Exception uncaught;
	
	private final Thread thread;
	
	public UncaughtExceptionEvent(Object source, Exception uncaught)
	{
		this.source = source;
		this.uncaught = uncaught;
		this.thread = Thread.currentThread();
	}
	
	public Object getSource()
	{
		return source;
	}
	
	public Exception getUncaughtException()
	{
		return uncaught;
	}
	
	public Thread getThread()
	{
		return thread;
	}
}
