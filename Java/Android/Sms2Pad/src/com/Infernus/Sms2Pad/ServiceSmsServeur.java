package com.Infernus.Sms2Pad;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.Set;
import java.util.TimeZone;
import java.util.UUID;

import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothServerSocket;
import android.bluetooth.BluetoothSocket;
import android.content.BroadcastReceiver;
import android.content.ContentValues;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.database.Cursor;
import android.os.Binder;
import android.os.Bundle;
import android.os.Handler;
import android.os.IBinder;
import android.telephony.gsm.SmsMessage;
import android.util.Log;

import com.Infernus.Sms2Pad.ServiceSmsClient.LocalBinder;

public class ServiceSmsServeur extends Service{
	private NotificationManager mNM;
	Handler handler;
	BroadcastReceiver broadcastReceiverSMS, broadcastReceiverEcran;
	
	ConnectedThread thread = null;
	ServeurBluetooth serveur = null;
	
	String nomAppareil;
	
	//Elements Bluetooth
	//BroadcastReceiver bluetoothReceiver=null;
	BluetoothAdapter bluetoothAdapter;
	BluetoothSocket socket=null;
	//boolean bluetoothReceiverOn=false;
	BluetoothDevice appar = null;
	UUID MY_UUID =
		UUID.fromString("00001105-0000-1000-8000-00805F9B34FC");
	
	public class LocalBinder extends Binder {
        ServiceSmsServeur getService() {
            return ServiceSmsServeur.this;
        }
    }
	
	@Override
	public void onStart(Intent intent, int startId){
		super.onStart(intent, startId);
		
		Log.i("register", "oui");
		nomAppareil = intent.getStringExtra("appareil");
	       //SmsManager.RESULT_ERROR_RADIO_OFF
	    bluetoothManaging();
	    connectThread();
	    thread = new ConnectedThread(socket, bluetoothAdapter, appar);
	    thread.run();
	       
		
		if(broadcastReceiverSMS == null){
			broadcastReceiverSMS = new BroadcastReceiver(){

				@Override
				public void onReceive(Context context, Intent intent) {
					String action = intent.getAction();
					Log.i("Envoyé", action.toString());
					Bundle bundle = intent.getExtras();
					SmsMessage[] messages = null;
					String expediteur = "";
					String body = "";
					if(bundle != null){
						Object[] pdus = (Object[])bundle.get("pdus");
						messages = new SmsMessage[pdus.length];
						for(int i=0; i<messages.length; ++i){
							messages[i] = SmsMessage.createFromPdu((byte[])pdus[i]);
							expediteur = messages[i].getOriginatingAddress();
							body = messages[i].getMessageBody().toString();
						}
					}
					connectThread();
					
					thread = new ConnectedThread(socket, bluetoothAdapter, appar);
					thread.run();
					ContentValues values = new ContentValues();
					values.put("bodyMessage", body);
		    		values.put("addressMessage", expediteur);
		    		long time = System.currentTimeMillis();
		    		
		    		/**TODO : Verifier le fonctionnement suivant l'heure été/hiver**/
		    		/*TimeZone timeZone = TimeZone.getDefault();
		            time += timeZone.getOffset(time);*/
		    		values.put("dateMessage", time);
		    		
					thread.write(values.toString().getBytes());
				}
			};
			Handler handler = new Handler();
			IntentFilter IF = new IntentFilter("android.provider.Telephony.SMS_RECEIVED");
		    registerReceiver(broadcastReceiverSMS, IF, null, handler);
		}
		if(broadcastReceiverEcran == null){
			broadcastReceiverEcran = new BroadcastReceiver(){

				@Override
				public void onReceive(Context context, Intent intent) {
					Log.i("Bluetooth", "Coupé");
				}
			};
			IntentFilter IF = new IntentFilter("android.bluetooth.adapter.action.STATE_CHANGED");
		    registerReceiver(broadcastReceiverEcran, IF, null, handler);
		}
	}
	
	@Override
    public void onCreate() {
        mNM = (NotificationManager)getSystemService(NOTIFICATION_SERVICE);
        // Display a notification about us starting.  We put an icon in the status bar.
        showNotification();
        
    }
	
	public void onDestroy(){
		super.onDestroy();
		mNM.cancel(5045);
		if(serveur.isAlive()){
			serveur.cancel();
		}
		unregisterReceiver(broadcastReceiverSMS);
		unregisterReceiver(broadcastReceiverEcran);
		if(thread!=null){
			thread.stop();
		}
	}
	
	public void showNotification(){
		Notification notification = new Notification(R.drawable.icon, "Serveur Actif", System.currentTimeMillis());
        PendingIntent pendingIntent = PendingIntent.getActivity(this, 0, new Intent(this, ServerSide.class), 0);
        notification.setLatestEventInfo(this, "Serveur Actif", "", pendingIntent);
        mNM.notify(5045, notification);
	}
	
	public void connectThread(){
		Set<BluetoothDevice> appareilsAssocies = bluetoothAdapter.getBondedDevices();
		for(BluetoothDevice appareil : appareilsAssocies){
			if(appareil.getName().contains(nomAppareil)){
				appar = appareil;
				try {
					socket = appareil.createRfcommSocketToServiceRecord(MY_UUID);
				} catch (IOException e) {
					Method m = null;
					try {
						m = appareil.getClass().getMethod("createRfcommSocket", new Class[] {int.class});
						socket = (BluetoothSocket) m.invoke(appareil, 1);
					} catch (SecurityException e1) {
						e1.printStackTrace();
					} catch (IllegalArgumentException b) {
						e.printStackTrace();
					} catch (InvocationTargetException e2) {
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
					} catch (IllegalAccessException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
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
					} catch (NoSuchMethodException e1) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
					e.printStackTrace();
				}
			}
		}
	}
	
	private final IBinder mBinder = new LocalBinder();
	@Override
	public IBinder onBind(Intent intent) {
		return mBinder;
	}
	
	private void bluetoothManaging(){
		bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
		final Set<BluetoothDevice> appareilsAssocies = bluetoothAdapter.getBondedDevices();
		if(appareilsAssocies.size()>0){
			/*bluetoothReceiver = new BroadcastReceiver(){

				@Override
				public void onReceive(Context context, Intent intent) {
					String action = intent.getAction();
					if(BluetoothDevice.ACTION_FOUND.equals(action)){
						BluetoothDevice appareilTrouvé = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
						for(BluetoothDevice appareil:appareilsAssocies){
							Log.i("Appareil Associé", "Nom : "+ appareil.getName()+" - MAC : " + appareil.getAddress());
							if(appareilTrouvé.equals(appareil)){
								Log.i("Appareil trouvé", "Nom : "+ appareil.getName()+" - MAC : " + appareil.getAddress());
								unregisterReceiver(this);
								bluetoothReceiverOn = false;
							}
						}
					}
				}
			};*/
			//do{
				Log.i("Serveur", "pret");
				createServerBluetooth();
			//}while(Sms2Pad.clientState);
			/*IntentFilter filtre = new IntentFilter(BluetoothDevice.ACTION_FOUND);
			registerReceiver(bluetoothReceiver, filtre);
			bluetoothReceiverOn = true;
			
			bluetoothAdapter.startDiscovery();*/
		}
	}
	
	public void createServerBluetooth(){
		synchronized(this){
			serveur = new ServeurBluetooth(bluetoothAdapter, this, mNM);
			serveur.start();
		}
	}
}

class ConnectedThread extends Thread {
    BluetoothSocket mmSocket=null;
    BluetoothAdapter bluetoothAdapter = null;
    BluetoothDevice appar = null;
    UUID MY_UUID =
		UUID.fromString("00001105-0000-1000-8000-00805F9B34FC");

    public ConnectedThread(BluetoothSocket socket, BluetoothAdapter adap, BluetoothDevice device) {
        
        // Get the BluetoothSocket input and output streams
        try {
        	appar = device;
        	mmSocket = appar.createRfcommSocketToServiceRecord(MY_UUID);
        	bluetoothAdapter=adap;
        } catch (IOException e) {
        }
    }

    public void run() {
    	byte[] buffer = new byte[1024];
        int bytes;
		try {
			if(bluetoothAdapter.isDiscovering()){
				bluetoothAdapter.cancelDiscovery();
			}
			mmSocket = appar.createRfcommSocketToServiceRecord(MY_UUID);
			mmSocket.connect();
		} catch (IOException e) {
			try {
				Method m = appar.getClass().getMethod("createRfcommSocket", new Class[] {int.class});
		        mmSocket = (BluetoothSocket) m.invoke(appar, 1);
			} catch (SecurityException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			} catch (NoSuchMethodException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
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
			Log.i("erreur 1", e.toString());
		}
    }

    /**
     * Write to the connected OutStream.
     * @param buffer  The bytes to write
     */
    public void write(byte[] buffer) {
        try {
        	mmSocket.getOutputStream().write(buffer);
        	mmSocket.close();
        } catch (IOException e) {
        	Log.i("erreur", e.toString());
        }
    }

    public void cancel() {
        try {
            mmSocket.close();
        } catch (IOException e) {
        }
    }
}