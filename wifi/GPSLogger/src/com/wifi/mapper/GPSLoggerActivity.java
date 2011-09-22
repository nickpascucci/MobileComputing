package com.wifi.mapper;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.util.List;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.view.View;
import android.widget.ProgressBar;
import android.widget.TextView;

public class GPSLoggerActivity extends Activity {
	/** Called when the activity is first created. */
	File file;
	OutputStream os;
	PrintWriter pw;
	TextView text;
	ProgressBar progress;
	WifiManager wifiMan;
	WifiReceiver receiverWifi;
	String latitude;
	String longitude;
	long startTime;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.main);
		// Set up file for writing
		String state = Environment.getExternalStorageState();
		if (Environment.MEDIA_MOUNTED.equals(state)) {
			file = new File(getExternalFilesDir(null), "WifiData.txt");
			Log.d("Filename: ", getExternalFilesDir(null).getAbsolutePath());
			try {
				os = new FileOutputStream(file);
				pw = new PrintWriter(os);
			} catch (FileNotFoundException e) {
				Log.d("outputstream", "file not found");
				e.printStackTrace();
			}
		} else {
			Log.d("Media mounting", "Unable to find SD card");
		}

		text = (TextView) findViewById(R.id.textView1);

		text.setText("Not running");

		progress = (ProgressBar) findViewById(R.id.progressBar1);
		progress.setVisibility(ProgressBar.INVISIBLE);
	}

	// ***May throw exception if print writer has been closed, but program still
	// running...
	public synchronized void updateLocation(Location location) {
		latitude = Double.toString(location.getLatitude());
		longitude = Double.toString(location.getLongitude());
	}

	public synchronized String getCoordinates() {
		return latitude + ", " + longitude;
	}

	public String getWifiData() {
		List<ScanResult> results = wifiMan.getScanResults();
		String networks = "";
		for (ScanResult sr : results) {
			// (Name, address, signal)
			networks += ", (" + sr.SSID + ", " + sr.BSSID + ", " + sr.level
					+ ")";
		}
		return networks;
	}

	// Initializes first line of file with time stamp, sets up location manager
	// and listener to start taking updates
	public synchronized void onGo(View v) {
		wifiMan = (WifiManager) this.getSystemService(Context.WIFI_SERVICE);
		receiverWifi = new WifiReceiver();
		LocationManager lmanage = (LocationManager) this
				.getSystemService(Context.LOCATION_SERVICE);

		LocationListener llisten = new LocationListener() {
			public void onLocationChanged(Location location) {
				updateLocation(location);
			}

			public void onStatusChanged(String provider, int status,
					Bundle extras) {
			}

			public void onProviderEnabled(String provider) {
			}

			public void onProviderDisabled(String provider) {
			}
		};

		// Update location every 5s
		lmanage.requestLocationUpdates(LocationManager.GPS_PROVIDER, 5000, 0,
				llisten);
		registerReceiver(receiverWifi, new IntentFilter(
				WifiManager.SCAN_RESULTS_AVAILABLE_ACTION));

		
		progress.setVisibility(ProgressBar.VISIBLE);
		text.setText("Starting to scan!");
		startTime = System.currentTimeMillis();
		wifiMan.startScan();
	}

	// Insert time stamp at stop location then write last coordinates, close
	// writer and output stream
	public synchronized void onEnd(View v) {

		pw.flush();
		try {
			os.flush();
		} catch (IOException e) {
			Log.d("output stream flush", "IO exception");
			e.printStackTrace();
		}
		pw.close();
		try {
			os.close();
		} catch (IOException e) {
			Log.d("output stream close", "IO exception");
			e.printStackTrace();
		}

		text.setText("Finishing...");

		finish();
	}

	private class WifiReceiver extends BroadcastReceiver {

		@Override
		public void onReceive(Context arg0, Intent arg1) {
			long endTime = System.currentTimeMillis();
			text.setText("Scan complete! Time: " + (endTime - startTime));
			String signal = getWifiData();
			String coordinates = getCoordinates();
			pw.println(coordinates + signal);
			progress.incrementProgressBy(1);
			//text.setText("Initiating new scan.");
			//wifiMan.startScan();
		}

	}
}