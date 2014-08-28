package com.LiveZoneStudio.skydiver;

import org.anddev.andengine.ui.activity.BaseActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class Menu extends BaseActivity{
	protected void onCreate(Bundle savedInstanceState){
		super.onCreate(savedInstanceState);
		
		setContentView(R.layout.main);
		
		Button startBouton = (Button)findViewById(R.id.start);
		startBouton.setOnClickListener(new View.OnClickListener() {
			
			@Override
			public void onClick(View v) {
				Intent intent = new Intent(Menu.this, SkyDiver.class);
				Menu.this.startActivity(intent);
			}
		});
		
		Button optionsBouton = (Button)findViewById(R.id.option);
	}
}
