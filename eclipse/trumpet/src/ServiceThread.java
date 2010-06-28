
public abstract class ServiceThread
implements Runnable
{
	private final UncaughtExceptionHandler exceptionHandler;
	
	private volatile Thread signal = null;

	public ServiceThread(UncaughtExceptionHandler exceptionHandler)
	{
		this.exceptionHandler = exceptionHandler;
	}

	public void run()
	{
		try
		{
			synchronized(this)
			{
				if(signal != null && signal.isAlive())
					throw new RuntimeException(
							"Service thread " + this + " is already running");
				signal = Thread.currentThread();
			}
			
			try 
			{
				runInternal();
			}
			catch(InterruptedException e)
			{
				signal = null;
				//#debug info
				System.out.println("Service thread " + this + 
						" was interrupted, service will now stop");
			}
		}
		catch(Throwable e)
		{
			//TODO: Remove, for debugging purposes only
			e.printStackTrace();
			exceptionHandler.handleUncaughtException(new UncaughtExceptionEvent(this, (Exception)e));
		}
	}

	public synchronized void stop()
	{
		if(signal == null || !signal.isAlive())
			throw new RuntimeException(
					"Service thread " + this + " is already stopped");
		//#debug info
		System.out.println("Stopping service thread " + this);
		signal.interrupt();
	}

	public synchronized void stopAndWait() throws InterruptedException
	{
		Thread signalLocal = signal;
		stop();
		//#debug info
		System.out.println("Waiting for service thread " + this + " to stop");
		signalLocal.join();
	}
	
	public boolean isRunning()
	{
		return signal != null && signal.isAlive();
	}
	
	protected abstract void runInternal()
	throws Exception;

}