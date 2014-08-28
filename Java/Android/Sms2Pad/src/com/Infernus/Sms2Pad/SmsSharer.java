package com.Infernus.Sms2Pad;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.telephony.gsm.SmsMessage;
import android.util.Log;

public class SmsSharer extends BroadcastReceiver{

	@Override
	public void onReceive(Context context, Intent intent) {
		String received = "android.provider.Telephony.SMS_RECEIVED";
		if(intent.getAction().equals(received)){
			Log.i("sms", "recu");
			
			Bundle bundle = intent.getExtras();
			SmsMessage[] messages = null;
			String str = "";
			if(bundle != null){
				Object[] pdus = (Object[])bundle.get("pdus");
				messages = new SmsMessage[pdus.length];
				for(int i=0; i<messages.length; ++i){
					messages[i] = SmsMessage.createFromPdu((byte[])pdus[i]);
					str += "SMS de " + messages[i].getOriginatingAddress();
					str += " :";
					str += messages[i].getMessageBody().toString();
					
					Log.i("Message", str);
				}
			}
		}
	}

}
