package com.Infernus.Sms2Pad;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.widget.Button;

public class Sms2Pad extends Activity {
    
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        //broadcastReceiver = (SmsSharer)savedInstanceState.get("broadcastReceiver");
        
        setContentView(R.layout.main);
        final Button client = (Button)findViewById(R.id.boutonClient);
        client.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View v){
				Intent i = new Intent(Sms2Pad.this, ClientSide.class);
				startActivity(i);
			}
		});
        
        Button serveur = (Button)findViewById(R.id.boutonServeur);
        serveur.setOnClickListener(new View.OnClickListener() {
			
			@Override
			public void onClick(View v) {
				Intent i = new Intent(Sms2Pad.this, ServerSide.class);
				startActivity(i);
			}
		});
    }
    
    public void onResume(){
    	super.onResume();
		
    }
    
    public void onDestroy(){
    	super.onDestroy();
    	
    }
}