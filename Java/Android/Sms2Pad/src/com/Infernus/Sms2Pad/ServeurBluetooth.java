package com.Infernus.Sms2Pad;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.UUID;

import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothServerSocket;
import android.bluetooth.BluetoothSocket;
import android.content.ContentValues;
import android.content.Context;
import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.telephony.SmsManager;
import android.util.Log;

class ServeurBluetooth extends Thread {
	private BluetoothServerSocket socketServeur=null;
	private BluetoothAdapter bluetoothAdap;
	private NotificationManager mNM;
	UUID MY_UUID =
		UUID.fromString("00001105-0000-1000-8000-00805F9B34FC");
	
	Context context;

    public ServeurBluetooth(BluetoothAdapter bluetoothAdapter, Context c, NotificationManager NM) {
        // On utilise un objet temporaire qui sera assigné plus tard à blueServerSocket car blueServerSocket est "final"
    	mNM=NM;
    	context = c;
        BluetoothServerSocket tmp = null;
        bluetoothAdap = bluetoothAdapter;
        try {
        	tmp = bluetoothAdap.listenUsingRfcommWithServiceRecord(".serviceSmsTest", MY_UUID);
        } catch (IOException e) { 
        	Log.i("Planté", "0");
        }
        socketServeur=tmp;
    }
    
    public ServeurBluetooth(BluetoothAdapter bluetoothAdapter, Context c) {
    	mNM=null;
    	context = c;
        BluetoothServerSocket tmp = null;
        bluetoothAdap = bluetoothAdapter;
        try {
        	tmp = bluetoothAdap.listenUsingRfcommWithServiceRecord(".serviceSmsTest", MY_UUID);
        } catch (IOException e) { 
        	Log.i("Planté", "0");
        }
        socketServeur=tmp;
    }
    
    private BluetoothSocket socket=null;
    
    @Override
    public void run(){
    	char[] buffer = new char[1];
        String body = "";
        String adresse = "";
        String date = "";
        
		while(true){
			try{
				Log.i("Listen", "yes");
				socket = socketServeur.accept();
				//Read from the InputStream
				
				if (socket != null) {
					try {
						InputStream is = socket.getInputStream();
						BufferedReader reader = new BufferedReader(new InputStreamReader(is));
						while((reader.read(buffer))!=-1){
							body += String.valueOf(buffer);
						}
					} catch (IOException e) {
						// TODO Auto-generated catch block
						Log.i("Lecteur", e.toString());
						Log.i("Lecteur", body);
					}
                    synchronized (this) {
        				//Parsing
        				int last;
        				Log.i("Message recu par bluetooth", new String(body));
        				last=body.lastIndexOf("addressMessage");
        				adresse=body.substring(last+15);
        				date=body.substring(body.lastIndexOf("dateMessage")+12, last-1);
        				Log.i("date", date);
        				last = body.lastIndexOf("dateMessage");
        				body=body.substring(12, last-1);
        				
        				if(date.length()<3){
        					Log.i("Chemin", "1");
        					nouveauEnvoiSMS(adresse, body);
        				}else{
        					Log.i("Chemin", "2");
        					nouveauSMS(adresse,date,body);
        				}
                    }
                }
			}catch(IOException e){
				try {
					this.finalize();
				} catch (Throwable e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
				}
				Log.i("Planté", e.toString());
				break;
			}
			break;
		}
	}
    
    public void nouveauSMS(String adresse, String date, String body){
        	try{
        		Uri uri = Uri.parse("content://sms/inbox");
        		Cursor c = context.getContentResolver().query(uri, null, null, null, null);
        		//c.move(1);
        		c.moveToFirst();
        		
        		ContentValues values = new ContentValues();
        		values.put("address", adresse);
        		values.put("person", "67");
        		values.put("date", date);
        		values.put("read", "0");
        		values.put("status", "-1");
        		values.put("type", "1");
        		values.put("body", body);
        		
        		context.getContentResolver().insert(uri, values);
        		
        		c.close();
        		showNotificationSms();
        		retry();
        	}catch(Exception e){
        		Log.i("erreur", e.toString());
        	}
        }
    
    public void nouveauEnvoiSMS(String adresse, String body){
    	try{
    		SmsManager.getDefault().sendTextMessage(adresse, null, body, null, null);
    		Uri uri = Uri.parse("content://sms/sent");
		    Cursor c = context.getContentResolver().query(uri, null, null, null, null);
		    c.moveToFirst();
		    
		    ContentValues values2 = new ContentValues();
      		values2.put("address", adresse);
      		//A vérifier
       		values2.put("date", System.currentTimeMillis());
       		values2.put("read", "1");
       		values2.put("status", c.getString(7));
       		values2.put("type", "2");
       		values2.put("body", body);
       		
       		context.getContentResolver().insert(uri, values2);
       		c.close();
    		Log.i("envoi", "oui");
    		retry();
    	}catch(Exception e){
    		Log.i("erreur", e.toString());
    	}
    }
    
    public void showNotificationSms(){
    	
		Notification notification = new Notification(R.drawable.icon, "Message Reçu", System.currentTimeMillis());
		//Intent i = new Intent("");
	    PendingIntent pendingIntent = PendingIntent.getActivity(context, 0, new Intent(context, ClientSide.class), 0);
	    notification.setLatestEventInfo(context, "Message Reçu", "", pendingIntent);
	    mNM.notify(5047, notification);
	}
    
    public void retry(){
    	if(this.isAlive()){
	    	cancel();
	    	try {
				socket.close();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
    	}
    	synchronized(this){
    		ServeurBluetooth serveur = new ServeurBluetooth(bluetoothAdap, context, mNM);
			serveur.start();
		}
    }
    
    public void write(byte[] buffer) {
        try {
            socket.getOutputStream().write(buffer);
            socket.close();
        } catch (IOException e) {
        	Log.i("erreur", e.toString());
        }
    }

    // On stoppe l'écoute des connexions et on tue le thread
    public void cancel(){
		try{
			if(socketServeur!=null){
				socketServeur.close();
			}
		}catch(IOException e){
			e.printStackTrace();
		}
	}
}
