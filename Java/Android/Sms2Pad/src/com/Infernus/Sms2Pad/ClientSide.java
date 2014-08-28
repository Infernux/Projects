package com.Infernus.Sms2Pad;

import java.util.ArrayList;
import java.util.Set;

import android.app.Activity;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.Handler;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.Toast;
import android.widget.AdapterView.OnItemClickListener;

public class ClientSide extends Activity{
	static boolean clientState = false;
	
	//ArrayList<String> listeAppareils = new ArrayList<String>();
	int selection=-1;
	String selectionName = null;
    
    public void onCreate(Bundle savedInstanceState){
    	super.onCreate(savedInstanceState);
    	
    	SharedPreferences preferences = getPreferences(Context.MODE_PRIVATE);
		selectionName=preferences.getString("clientName", null);
    	
    	final BluetoothAdapter bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
    	
		setContentView(R.layout.menu);
    	
    	final Button client = (Button)findViewById(R.id.active);
        client.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View v){
				if(clientState){
					clientState=false;
					Intent i = new Intent(ClientSide.this, ServiceSmsClient.class);
					ClientSide.this.stopService(i);
					client.setText("Client désactivé");
				}else{
					if(bluetoothAdapter.isEnabled()){
						if(selectionName!=null){
							clientState=true;
							Intent i = new Intent(ClientSide.this, ServiceSmsClient.class);
							i.putExtra("appareil", selectionName);
							ClientSide.this.startService(i);
							client.setText("Client activé");
						}else{
								Toast.makeText(v.getContext(), "Selectionnez un appareil", 4000).show();
						}
					}else{
						Toast.makeText(v.getContext(), "Activez le bluetooth", 4000).show();
					}
				}
			}
		});
        if(clientState){
        	client.setText("Client Activé");
        }else{
        	client.setText("Client Desactivé");
        }
        
        RadioGroup group = (RadioGroup)findViewById(R.id.groupRadio);
        group.setOrientation(LinearLayout.VERTICAL);
        
        group.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {
			
			@Override
			public void onCheckedChanged(RadioGroup group, int checkedId) {
				RadioButton tmpRB = (RadioButton)group.findViewById(checkedId);
				selectionName = tmpRB.getText().toString();
				//selectionName = listeAppareils.get(group.getCheckedRadioButtonId());
			}
		});
        
        /*ListView liste = (ListView)findViewById(R.id.liste);
        
        ListAdapter adapter = new ListAdapter(this, listeAppareils);
		liste.setAdapter(adapter);*/
        Set<BluetoothDevice> appareilsAssocies = bluetoothAdapter.getBondedDevices();
        for(BluetoothDevice b:appareilsAssocies){
        	RadioButton tmpRB = new RadioButton(this);
        	tmpRB.setText(b.getName());
        	group.addView(tmpRB);
        	if(selectionName!=null){
	        	if(b.getName().contains(selectionName)){
	        		tmpRB.setChecked(true);
	        	}
        	}
        }
    }
    
    @Override
	public void onStop(){
		super.onStop();
		SharedPreferences preferences = getPreferences(Context.MODE_PRIVATE);
		SharedPreferences.Editor editor = preferences.edit();
		editor.putString("clientName", selectionName);
		editor.commit();
	}
    
    public void onRestoreInstanceState(Bundle savedInstanceState){
    	super.onRestoreInstanceState(savedInstanceState);
    	clientState = savedInstanceState.getBoolean("serveurActif", false);
    	selectionName = savedInstanceState.getString("clientName");
    }
    
    public void onSaveInstanceState(Bundle outState){
    	super.onSaveInstanceState(outState);
    	outState.putBoolean("serveurActif", clientState);
    	outState.putString("clientName", selectionName);
    }
    
    /*class ListAdapter extends ArrayAdapter<String>{
		Activity context;
		
		ListAdapter(Activity context, ArrayList<String> list) {
			super(context, R.layout.rowbluetoothlist, list);
			
			this.context=context;
		}
		
		public View getView(final int position, View convertView,	ViewGroup parent) {
			View row=convertView;
			ViewWrapper wrapper;
												
													
			if (row==null) {		
				LayoutInflater inflater=context.getLayoutInflater();
				
				row=inflater.inflate(R.layout.rowbluetoothlist, null);
				wrapper=new ViewWrapper(row);
				row.setTag(wrapper);
				
			}
			else {
				wrapper=(ViewWrapper)row.getTag();
			}
			
			RadioButton radio = wrapper.getSelecteur();
			
			radio.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
				
				@Override
				public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
					selectionName = listeAppareils.get(position);
				}
			});
			
			wrapper.getNom().setText(listeAppareils.get(position));
			if(selection==position){
				wrapper.getSelecteur().setChecked(true);
			}
			return(row);
		}
		
	}*/
}