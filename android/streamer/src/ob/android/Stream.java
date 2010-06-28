package ob.android;

import static ob.android.Constants.*;
import jnix.Pipe;

public class Stream
implements Runnable
{
	private final Pipe video;
	
	private final Pipe audio;
	
	public Stream(Pipe video, Pipe audio)
	{
		this.video = video;
		this.audio = audio;
	}
	
	public void run()
	{
		debug("Stream started");
		stream();
		video.closeInput();
		audio.closeInput();
		debug("Stream finished");
	}
	
	private native void stream();
}
