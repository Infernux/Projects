package com.Infernus.Sms2Pad;

import java.util.ArrayList;
import java.util.Set;
import android.app.Activity;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
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
import android.widget.CompoundButton.OnCheckedChangeListener;

public class ServerSide extends Activity{
	
	static boolean serveurState = false;

	ArrayList<String> listeAppareils = new ArrayList<String>();
	String selectionName=null;
	int selection=-1;
	
	public void onCreate(Bundle bundle){
		super.onCreate(bundle);
		
		SharedPreferences preferences = getPreferences(Context.MODE_PRIVATE);
		selectionName=preferences.getString("serveurName", null);
		
		final BluetoothAdapter bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
	
		setContentView(R.layout.menu);
		
		final Button serveur = (Button)findViewById(R.id.active);
		
		serveur.setOnClickListener(new View.OnClickListener() {
			
			@Override
			public void onClick(View v) {
				if(serveurState){
					serveurState=false;
					Intent i = new Intent(ServerSide.this, ServiceSmsServeur.class);
					ServerSide.this.stopService(i);
					serveur.setText("Serveur Désactivé");
				}else{
					if(bluetoothAdapter.isEnabled()){
						if(selectionName!=null){
							Intent i = new Intent(ServerSide.this, ServiceSmsServeur.class);
							i.putExtra("appareil", selectionName);
							serveurState=true;
							ServerSide.this.startService(i);
							serveur.setText("Serveur activé");
						}
						else{
							Toast.makeText(v.getContext(), "Selectionnez un appareil", 4000).show();
						}
					}else{
						Toast.makeText(v.getContext(), "Activez le bluetooth", 4000).show();
					}
				}
			}
		});
		
		if(serveurState){
        	serveur.setText("Serveur Activé");
        }else{
        	serveur.setText("Serveur Desactivé");
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
        
        Set<BluetoothDevice> appareilsAssocies = bluetoothAdapter.getBondedDevices();
        for(BluetoothDevice b:appareilsAssocies){
        	RadioButton tmpRB = new RadioButton(this);
        	tmpRB.setText(b.getName());
        	group.addView(tmpRB);
        	listeAppareils.add(b.getName());
        	if(selectionName!=null){
	        	if(b.getName().contains(selectionName)){
	        		tmpRB.setChecked(true);
	        	}
        	}
        }
	}
	
	@Override
	public void onResume(){
		super.onResume();
	}
		
	@Override
	public void onStop(){
		super.onStop();
		SharedPreferences preferences = getPreferences(Context.MODE_PRIVATE);
		SharedPreferences.Editor editor = preferences.edit();
		editor.putString("serveurName", selectionName);
		editor.commit();
	}
	
	@Override
	protected void onRestoreInstanceState(Bundle savedInstanceState){
    	super.onRestoreInstanceState(savedInstanceState);
    	serveurState = savedInstanceState.getBoolean("serveurActif", false);
    	selectionName = savedInstanceState.getString("serveurName");
    }
    
	@Override
	protected void onSaveInstanceState(Bundle outState){
    	super.onSaveInstanceState(outState);
    	outState.putBoolean("serveurActif", serveurState);
    	outState.putString("serveurName", selectionName);
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