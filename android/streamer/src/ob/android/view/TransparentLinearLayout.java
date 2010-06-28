package ob.android.view;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.RectF;
import android.graphics.Paint.Style;
import android.util.AttributeSet;
import android.widget.LinearLayout;

public class TransparentLinearLayout 
extends LinearLayout
{
    private final Paint borderPaint = new Paint();;
    
    private final Paint backgroundPaint = new Paint();
    
    public TransparentLinearLayout(Context context)
    {
        super(context);
        init();       
    }
    
    public TransparentLinearLayout(Context context, AttributeSet attrs)
    {
        super(context, attrs);
        init();       
    }
    
    private void init()
    {
        backgroundPaint.setARGB(100, 0, 0, 0);
        backgroundPaint.setAntiAlias(true);
        
        borderPaint.setARGB(255, 200, 200, 200);
        borderPaint.setAntiAlias(true);
        borderPaint.setStyle(Style.STROKE);
        borderPaint.setStrokeWidth(2);
    }

    @Override
    protected void dispatchDraw(Canvas canvas)
    {
        RectF drawRect = new RectF();
        drawRect.set(0,0, getMeasuredWidth(), getMeasuredHeight());                
        canvas.drawRoundRect(drawRect, 5, 5, backgroundPaint);
        canvas.drawRoundRect(drawRect, 5, 5, borderPaint);
        super.dispatchDraw(canvas);
    }
}
