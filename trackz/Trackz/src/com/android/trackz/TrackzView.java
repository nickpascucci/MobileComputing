package com.android.trackz;

import android.content.Context;
import android.view.MotionEvent;
import android.view.SurfaceView;
import android.view.View;

public class TrackzView extends SurfaceView {
	
	TrackzActivity mainactivity;
	
	public TrackzView(Context context) {
		super(context);
		this.mainactivity = (TrackzActivity) context;
		
	}

	
}
