package com.Infernus.Sms2Pad;

import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.Set;
import java.util.UUID;

import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;

import android.content.BroadcastReceiver;
import android.content.ContentValues;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.database.ContentObserver;
import android.database.Cursor;
import android.net.Uri;
import android.os.Binder;
import android.os.Handler;
import android.os.IBinder;
import android.util.Log;

public class ServiceSmsClient extends Service{
	private NotificationManager mNM;
	//Task
	//OutBoxTask task = null;
	SMSObserver smsObserver=null;
	//Timer timer = new Timer();
	ServeurBluetooth serveur;
	ConnectedThread thread = null;
	
	String nomAppareil = null;
	
	//Elements Bluetooth
	BluetoothSocket socket=null;
	BluetoothDevice appar = null;
	UUID MY_UUID =
		UUID.fromString("00001105-0000-1000-8000-00805F9B34FC");
	BroadcastReceiver bluetoothReceiver, broadcastReceiverEcran=null;
	BluetoothAdapter bluetoothAdapter;
	boolean bluetoothReceiverOn=false;
	
	public class LocalBinder extends Binder {
        ServiceSmsClient getService() {
            return ServiceSmsClient.this;
        }
    }
	
	@Override
	public void onStart(Intent intent, int startId){
		super.onStart(intent, startId);
		bluetoothManaging();
		nomAppareil = intent.getStringExtra("appareil");
		
		Handler handler = new Handler();
		
		if(broadcastReceiverEcran == null){
			broadcastReceiverEcran = new BroadcastReceiver(){
				@Override
				public void onReceive(Context context, Intent intent){
					if(bluetoothAdapter.isEnabled()==true){
						bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
						createServerBluetooth();
					}else{
						serveur.cancel();
					}
				}
			};
			IntentFilter IF = new IntentFilter("android.bluetooth.adapter.action.STATE_CHANGED");
		    registerReceiver(broadcastReceiverEcran, IF, null, handler);
		}
		
		Log.i("register", "oui");
        
        Uri uri = Uri.parse("content://sms/");
        handler = new Handler();
        smsObserver = new SMSObserver(handler, this);
        getContentResolver().registerContentObserver(uri, true, smsObserver);
	}
	
	@Override
    public void onCreate() {
        mNM = (NotificationManager)getSystemService(NOTIFICATION_SERVICE);
        bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        
        showNotification();
    }
	
	public void showNotification(){
		mNM = (NotificationManager)getSystemService(NOTIFICATION_SERVICE);
        Notification notification = new Notification(R.drawable.icon, "Client Actif", System.currentTimeMillis());
        PendingIntent pendingIntent = PendingIntent.getActivity(this, 0, new Intent(this, ClientSide.class), 0);
        notification.setLatestEventInfo(this, "Client Actif", "", pendingIntent);
        mNM.notify(5046, notification);
	}
	
	public void onDestroy(){
		super.onDestroy();
		if(serveur!=null){
			if(serveur.isAlive()){
				serveur.cancel();
			}
		}
		mNM.cancel(5046);
		mNM.cancel(5047);
		if(bluetoothReceiverOn){
			unregisterReceiver(bluetoothReceiver);
		}
		unregisterReceiver(broadcastReceiverEcran);
		getContentResolver().unregisterContentObserver(smsObserver);
	}
	
	private final IBinder mBinder = new LocalBinder();
	@Override
	public IBinder onBind(Intent intent) {
		return mBinder;
	}
	
	private void bluetoothManaging(){
		final Set<BluetoothDevice> appareilsAssocies = bluetoothAdapter.getBondedDevices();
		if(appareilsAssocies.size()>0){
			Log.i("Serveur", "pret");
			createServerBluetooth();
		}
	}
	
	public void connectThread(){
		
		Set<BluetoothDevice> appareilsAssocies = bluetoothAdapter.getBondedDevices();
		for(BluetoothDevice appareil : appareilsAssocies){
			if(appareil.getName().contains(nomAppareil)){
				appar = appareil;
				try {
					Log.i("Passage", "Ici");
					socket = appareil.createRfcommSocketToServiceRecord(MY_UUID);
				} catch (IOException e) {
					Method m = null;
					try {
						m = appareil.getClass().getMethod("createRfcommSocket", new Class[] {int.class});
						socket = (BluetoothSocket) m.invoke(appareil, 1);
					} catch (SecurityException e1) {
						e1.printStackTrace();
					} catch (NoSuchMethodException e1) {
						e1.printStackTrace();
					} catch (InvocationTargetException e2) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					} catch (IllegalArgumentException e1) {
						// TODO Auto-generated catch block
						e.printStackTrace();
						try {
							socket = (BluetoothSocket) m.invoke(appareil, 2);
						} catch (IllegalArgumentException e2) {
							// TODO Auto-generated catch block
							e2.printStackTrace();
						} catch (IllegalAccessException e2) {
							// TODO Auto-generated catch block
							e2.printStackTrace();
						} catch (InvocationTargetException e2) {
							// TODO Auto-generated catch block
							e2.printStackTrace();
						}
					} catch (IllegalAccessException e2) {
						// TODO Auto-generated catch block
						e.printStackTrace();
						try {
							socket = (BluetoothSocket) m.invoke(appareil, 2);
						} catch (IllegalArgumentException e1) {
							// TODO Auto-generated catch block
							e1.printStackTrace();
						} catch (IllegalAccessException e1) {
							// TODO Auto-generated catch block
							e1.printStackTrace();
						} catch (InvocationTargetException e1) {
							// TODO Auto-generated catch block
							e1.printStackTrace();
						}
					}
					e.printStackTrace();
				}
			}
		}
	}
	
	public void createServerBluetooth(){
		synchronized(this){
			serveur = new ServeurBluetooth(bluetoothAdapter, this, mNM);
			serveur.start();
		}
	}
	
	class SMSObserver extends ContentObserver {
		Context context;
		
		public SMSObserver(final Handler smshandle, Context c) {
			super(smshandle);
			context=c;
		}

		public void onChange(final boolean bSelfChange) {
			super.onChange(bSelfChange);
			if(!bSelfChange){
				try {
					Uri uri = Uri.parse("content://sms/");
				    Cursor c = context.getContentResolver().query(uri, null, null, null, null);
				    c.moveToFirst();
				    for(int i=0; i<c.getColumnCount(); ++i){
				    	if(c.getString(i)!=null){
				    		Log.i(c.getColumnName(i),c.getString(i));
				    	}
				    }
		    		if(!(c.getString(8).contains("1")||c.getString(8).contains("2"))){
			    		connectThread();
			    		thread = new ConnectedThread(socket, bluetoothAdapter, appar);
						thread.run();
						
						ContentValues values = new ContentValues();
						values.put("bodyMessage", c.getString(11));
			    		values.put("addressMessage", c.getString(2));
			    		values.put("dateMessage", "");
						
						ContentValues values2 = new ContentValues();
			      		values2.put("address", c.getString(2));
			       		values2.put("date", c.getString(4));
			       		values2.put("read", "1");
			       		values2.put("status", c.getString(7));
			       		values2.put("type", "2");
			       		values2.put("body", c.getString(11));
			        		
			       		context.getContentResolver().delete(uri, "_id = "+c.getString(0), null);
			    		
			    		thread.write(values.toString().getBytes());
			       		Log.i("J'envoie","Ici");
						
			       		c.close();
			       		
			       		uri = Uri.parse("content://sms/sent");
				    	c = context.getContentResolver().query(uri, null, null, null, null);
			        		
			       		context.getContentResolver().insert(uri, values2);
			       		for(int i=0; i<c.getColumnCount(); ++i){
					    	if(c.getString(i)!=null){
					    		Log.i(c.getColumnName(i),c.getString(i));
					    	}
					    }
			       		c.close();
			    	}
			    	c.close();
				} catch (Exception e) {
					Log.i("test","SMSMonitor");
				}
			}
		}
	}
}