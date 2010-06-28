package ob.android.view;

import java.io.IOException;

import ob.android.Constants;

import android.content.Context;
import android.hardware.Camera;
import android.view.SurfaceHolder;
import android.view.SurfaceView;

public class CameraPreview 
extends SurfaceView
implements SurfaceHolder.Callback
{
	private final Object surfaceCreationSync = new Object();
	
	private final Object surfaceChangedSync = new Object();
	
	private Camera camera;
	
	private SurfaceHolder surfaceCreatedHolder;
	
	private boolean surfaceWasChanged = false;
	
	private int width;
	
	private int height;

	public CameraPreview(Context context)
	{
		super(context);
		SurfaceHolder holder = getHolder();
		holder.addCallback(this);
		holder.setType(SurfaceHolder.SURFACE_TYPE_PUSH_BUFFERS);
	}

	public void surfaceCreated(SurfaceHolder holder)
	{
		Constants.debug("surfaceCreated start");
		synchronized(surfaceCreationSync)
		{
			surfaceCreatedHolder = holder;
			surfaceCreationSync.notifyAll();
		}
		Constants.debug("surfaceCreated end");
	}

	public void surfaceDestroyed(SurfaceHolder holder)
	{
		stopPreview();
	}

	public void surfaceChanged(SurfaceHolder holder, int format, int width, int height)
	{
		synchronized(surfaceChangedSync)
		{
			surfaceWasChanged = true;
			this.width = width;
			this.height = height;
			surfaceChangedSync.notifyAll();
		}
	}
	
	public void stopPreview()
	{
		if(camera == null)
			throw new RuntimeException();
		camera.stopPreview();
		camera.release();
		camera = null;
	}
	
	public void startPreview()
	throws IOException
	{
	    new Thread(new Runnable()
        {
            
            public void run()
            {
                if(camera != null)
                    throw new RuntimeException();
                camera = Camera.open();
                synchronized(surfaceCreationSync)
                {
                    while(surfaceCreatedHolder == null)
                        try { surfaceCreationSync.wait(); }
                        catch (InterruptedException e) { /* */ }
                    try
                    {
                        camera.setPreviewDisplay(surfaceCreatedHolder);
                    } catch (IOException e)
                    {
                        throw new RuntimeException(e);
                    }
                }
                synchronized(surfaceChangedSync)
                {
                    while(!surfaceWasChanged)
                        try { surfaceChangedSync.wait(); }
                        catch (InterruptedException e) { /* */ }
                    Camera.Parameters parameters = camera.getParameters();
                    parameters.setPreviewFrameRate(25);
                    parameters.setPreviewSize(width, height);
                    camera.setParameters(parameters);
                }       
                camera.startPreview();
            }
        }).start();
	}
}
