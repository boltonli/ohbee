package ob.android.view;

import java.util.Observable;
import java.util.Observer;

import ob.android.Action;
import ob.android.model.Model;
import android.content.Context;
import android.graphics.Color;
import android.view.Gravity;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.ToggleButton;

public class ViewFactory
{
    private final Model model;
    
    private final Context context;
    
    public ViewFactory(Model model, Context context)
    {
        this.model = model;
        this.context = context;
    }
    
    public View getButtonView(final Action onAction, final Action offAction)
    {
        LinearLayout layout = new LinearLayout(context);
        layout.setGravity(Gravity.CENTER_HORIZONTAL);
        
        final ToggleButton button = new ToggleButton(context);
        button.setTextOff("Stopped");
        button.setTextOn("Recording");
        button.setOnClickListener(new View.OnClickListener()
        {
            public void onClick(View v)
            {
                if(button.isChecked())
                    onAction.doAction();
                else
                    offAction.doAction(); 
            }
        });
        
        layout.addView(button);
        
        return layout;
    }
    
    public View getGPSView()
    {
        final TextView view = new TextView(context);
        view.setTextColor(Color.GREEN);
        view.setText("Waiting for GPS");
        Observer observer = new Observer()
        {
            public void update(Observable observable, Object data)
            {
                if(data != Model.MODEL_CHANGE_KEYS.LOCATION)
                    return;
                String location = String.format(
                        "Latitude: %f\nLongitude: %f\nAccuracy: %.2fm",
                        model.getLocation().getLatitude().doubleValue(),
                        model.getLocation().getLatitude().doubleValue(),
                        model.getLocation().getLatitude().doubleValue());
                view.setText(location);
            }
        };
        model.addObserver(observer);
                
        LinearLayout linearLayout = new TransparentLinearLayout(context);
        linearLayout.setPadding(5, 5, 5, 5);
        linearLayout.setOrientation(LinearLayout.VERTICAL);
        linearLayout.addView(view);
        
        return linearLayout;
    }
    
    public View getCompassView()
    {
        final TextView view = new TextView(context);
        view.setTextColor(Color.GREEN);
        view.setText("Waiting for compass");
        Observer observer = new Observer()
        {
            public void update(Observable observable, Object data)
            {
                if(data != Model.MODEL_CHANGE_KEYS.ORIENTATION)
                    return;
                view.setText(String.format(
                        "Compass: %.2f", 
                        model.getOrientation().getAzimuth()));
            }
        };
        model.addObserver(observer);
       
        LinearLayout linearLayout = new TransparentLinearLayout(context);
        linearLayout.setPadding(5, 5, 5, 5);
        linearLayout.setOrientation(LinearLayout.VERTICAL);
        linearLayout.addView(view);
        
        return linearLayout;
    }
}
