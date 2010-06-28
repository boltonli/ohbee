package ob.android;

import java.io.IOException;

import jnix.Pipe;

import ob.android.model.Model;
import ob.android.model.ModelUtility;
import ob.android.view.CameraPreview;
import ob.android.view.ViewFactory;

import android.app.Activity;
import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.media.MediaRecorder;
import android.os.Bundle;
import android.view.Gravity;
import android.view.Window;
import android.view.WindowManager;
import android.widget.FrameLayout;
import android.widget.LinearLayout;

import static ob.android.Constants.*;

public class MainActivity
extends Activity
{	
    static
    {
        try
        {
            System.loadLibrary("jnix");
            System.loadLibrary("streamer");
        }
        catch(Throwable e)
        {
            error(e.getMessage(), e);
            throw new RuntimeException(e);
        }
    }
    
	private CameraPreview cameraPreview;
	
	private Pipe videoPipe = new Pipe();
	
	private Pipe audioPipe = new Pipe();
	
	private MediaRecorder videoRecorder;
	
	private MediaRecorder audioRecorder;
		
	@Override
	public void onCreate(Bundle savedInstanceState)
	{
		super.onCreate(savedInstanceState);
		debug("onCreate");
		
        cameraPreview = new CameraPreview(this);
          
        LinearLayout controlLayout = new LinearLayout(this);
        controlLayout.setOrientation(LinearLayout.VERTICAL);
                
        final Model model = new Model("android1");
        final ModelUtility modelUtility = new ModelUtility();
        
        LocationManager locationManager = (LocationManager)getSystemService(Context.LOCATION_SERVICE);
        locationManager.requestLocationUpdates(
                LocationManager.GPS_PROVIDER, 
                0,
                0, 
                new LocationListener()
                {
                    public void onStatusChanged(String provider, int status, Bundle extras){}
                    
                    public void onProviderEnabled(String provider){}
                    
                    public void onProviderDisabled(String provider){}
                    
                    public void onLocationChanged(Location location)
                    {
                        modelUtility.updateLocation(location, model);
                    }
                });
        
        SensorManager sensorManager = (SensorManager)getSystemService(Context.SENSOR_SERVICE);
        sensorManager.registerListener(
                new SensorEventListener()
                {
                    public void onSensorChanged(SensorEvent event)
                    {
                        modelUtility.updateOrientation(
                                new Double(event.values[0]), 
                                new Double(event.values[1]),
                                new Double(event.values[2]),
                                model);                                          
                    }
                    
                    public void onAccuracyChanged(Sensor sensor, int accuracy){}
                }, 
                sensorManager.getDefaultSensor(Sensor.TYPE_ORIENTATION),
                SensorManager.SENSOR_DELAY_NORMAL);
        
        ViewFactory viewFactory = new ViewFactory(model, this);
        
        controlLayout.addView(viewFactory.getGPSView());
        controlLayout.addView(viewFactory.getCompassView());
        controlLayout.addView(viewFactory.getButtonView(new Action()
        {
            public void doAction()
            {
                MainActivity.this.startRecording();
            }
        }, new Action()
        {
            
            public void doAction()
            {
                MainActivity.this.stopRecording();
            }
        }));
        
        LinearLayout controlLayer = new LinearLayout(this);
        controlLayer.setGravity(Gravity.RIGHT);
        controlLayer.addView(controlLayout);
        
        FrameLayout mainLayout = new FrameLayout(this);
        mainLayout.addView(cameraPreview);
        mainLayout.addView(controlLayer);

        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, 
                                WindowManager.LayoutParams.FLAG_FULLSCREEN);
        
        setContentView(mainLayout);
	}
	
	@Override
	protected void onDestroy()
	{
		super.onDestroy();
		debug("onDestroy");
	}

	@Override
	protected void onPause()
	{
		super.onPause();
		debug("onPause");
		System.exit(0);
	}

	@Override
	protected void onRestart()
	{
		super.onRestart();
		debug("onRestart");
	}

	@Override
	protected void onResume()
	{
		super.onResume();
		debug("onResume");
		try
        {
            cameraPreview.startPreview();
        }
		catch(IOException e)
        {
            error("Unable to start the camera preview", e);
            throw new RuntimeException(e);
        }
	}

	@Override
	protected void onStart()
	{
		super.onStart();
		debug("onStart");
		
	}

	@Override
	protected void onStop()
	{
		super.onStop();
		debug("onStop");
	}
	
	
	
	private void startRecording()
    {
        Thread t = new Thread(new Stream(videoPipe, audioPipe));
        t.setPriority(Thread.MAX_PRIORITY);
        t.start();
                
        try
        {
            cameraPreview.stopPreview();
            
            videoRecorder = new MediaRecorder();
            videoRecorder.setPreviewDisplay(cameraPreview.getHolder().getSurface());
            videoRecorder.setVideoSource(MediaRecorder.VideoSource.CAMERA);
            videoRecorder.setOutputFormat(MediaRecorder.OutputFormat.MPEG_4);
            videoRecorder.setVideoEncoder(MediaRecorder.VideoEncoder.MPEG_4_SP);
            videoRecorder.setVideoSize(320, 240);
            videoRecorder.setVideoFrameRate(15);
            videoRecorder.setOutputFile(videoPipe.getOutput());
            videoRecorder.prepare();
            videoRecorder.start();
            
            audioRecorder = new MediaRecorder();
            audioRecorder.setAudioSource(MediaRecorder.AudioSource.MIC);
            audioRecorder.setOutputFormat(MediaRecorder.OutputFormat.RAW_AMR);
            audioRecorder.setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB);
            audioRecorder.setOutputFile(audioPipe.getOutput());
            audioRecorder.prepare();
            audioRecorder.start();
        }
        catch(Exception e)
        {
            error("Unable to start recording", e);
        }
    }
    
    private void stopRecording()
    {
        videoRecorder.stop();
        videoRecorder.release();
        videoPipe.closeOutput();
        audioPipe.closeOutput();
        try
        {
            cameraPreview.startPreview();
        } catch (IOException e)
        {
            error("Unable to start camera preview", e);
        }
    }
}
