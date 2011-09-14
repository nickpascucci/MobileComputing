package com.android.trackz;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.HashSet;
import java.util.Set;
import java.util.UUID;

import android.app.Activity;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.widget.Toast;

public class TrackzActivity extends Activity {

	private static final UUID MY_UUID = UUID
			.fromString("2f5ffe67-81f1-4e9b-8636-370b83607639");	
	private static final int REQUEST_ENABLE_BT = 3;
	Set<BluetoothDevice> addresses = new HashSet<BluetoothDevice>();
	private BluetoothSocket connection;
	BluetoothAdapter adapter;
	BroadcastReceiver receiver;

	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.main);

		adapter = BluetoothAdapter.getDefaultAdapter();
		if (adapter == null) {
			finish();
			return;
		} else {
			Toast.makeText(this, "Bluetooth available, finding host",
					Toast.LENGTH_SHORT).show();
			
			getConnections(adapter);
			IntentFilter filter = new IntentFilter(BluetoothDevice.ACTION_FOUND);
			IntentFilter discovery = new IntentFilter(BluetoothAdapter.ACTION_DISCOVERY_FINISHED);
			registerReceiver(receiver, filter);
			registerReceiver(receiver, discovery);
			Toast.makeText(getApplicationContext(), "Beginning discovery",
					Toast.LENGTH_SHORT).show();
			adapter.startDiscovery();
		}
	}

	public void getConnections(BluetoothAdapter ba) {

		if (!ba.isEnabled()) {
			Intent enableBt = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
			startActivityForResult(enableBt, REQUEST_ENABLE_BT);
			Toast.makeText(this, "Enabling Bluetooth", Toast.LENGTH_LONG)
					.show();
		}

		// Create a BroadcastReceiver for ACTION_FOUND
		receiver = new BroadcastReceiver() {
			public void onReceive(Context context, Intent intent) {
				String action = intent.getAction();
				// When discovery finds a device
				if (BluetoothDevice.ACTION_FOUND.equals(action)) {
					// Get the BluetoothDevice object from the Intent
					BluetoothDevice device = intent
							.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
					// Add the name and address to an array adapter to show in a
					// ListView
					Toast.makeText(getApplicationContext(),
							"Found device " + device.getName(),
							Toast.LENGTH_SHORT).show();
					addresses.add(device);
				}
				else if (BluetoothAdapter.ACTION_DISCOVERY_FINISHED.equals(action) && addresses.size() > 0) {
					makeConnection();
				}
			}
		};
	}

	public void makeConnection() {
		BluetoothSocket tmp = null;
		adapter.cancelDiscovery();
		for (BluetoothDevice device : addresses) {
			try {
				tmp = device.createInsecureRfcommSocketToServiceRecord(MY_UUID);
				Toast.makeText(this, "Made socket for " + device.getName(), Toast.LENGTH_SHORT).show();
				tmp.connect();
				Toast.makeText(this, "Managed to connect to " + device.getName(), Toast.LENGTH_SHORT).show();
				OutputStream os = tmp.getOutputStream();
				InputStream is = tmp.getInputStream();
				os.write("TRACKZ".getBytes());
				byte[] bytes = new byte[6];
				is.read(bytes);
				String handshake = new String(bytes);
				if (handshake.equalsIgnoreCase("TRACKZ")) {
					Toast.makeText(this, "Connected to host", Toast.LENGTH_LONG)
							.show();
					break;
				} else {
					tmp.close();
				}
			} catch (IOException e) {
				Toast.makeText(this, "Error: " + e.getMessage() + " on " + device.getName(), Toast.LENGTH_SHORT).show();
			}
		}
		connection = tmp;
	}
	
	public void onDestroy() {
		super.onDestroy();
		unregisterReceiver(receiver);
	}
}
