package com.OrkCreation.LiveWallpaper;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.Preference;
import android.preference.PreferenceActivity;
import android.preference.Preference.OnPreferenceClickListener;
import android.util.Log;

public class Orkloge_settings extends PreferenceActivity
    implements SharedPreferences.OnSharedPreferenceChangeListener{
	
	SharedPreferences mSharedPreferences;

    @Override
    protected void onCreate(Bundle icicle) {
        super.onCreate(icicle);
        getPreferenceManager().setSharedPreferencesName(
                OrkLiveWallpaper.SHARED_PREFS_NAME);
        mSharedPreferences = getSharedPreferences(OrkLiveWallpaper.SHARED_PREFS_NAME, MODE_PRIVATE);
        addPreferencesFromResource(R.xml.orkloge_settings);
        getPreferenceManager().getSharedPreferences().registerOnSharedPreferenceChangeListener(this);
        Preference pref = this.getPreferenceScreen().getPreference(2);
        pref.setOnPreferenceClickListener(new OnPreferenceClickListener() {
			
			@Override
			public boolean onPreferenceClick(Preference preference) {
				lanceIntent();
				return false;
			}
		});
        
    }

    @Override
    protected void onResume() {
        super.onResume();
    }

    @Override
    protected void onDestroy() {
        getPreferenceManager().getSharedPreferences().unregisterOnSharedPreferenceChangeListener(
                this);
        super.onDestroy();
    }
    
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data){
    	super.onActivityResult(requestCode, resultCode, data);
    	if(resultCode==-1){
    		//Image choisie
    		SharedPreferences.Editor edit = mSharedPreferences.edit();
    		edit.putString("fond", data.getDataString());
    		edit.commit();
    	}else{
    		//Pas d'image choisie
    	}
    }
    
    public void lanceIntent(){
    	Intent i = new Intent();
        i.setAction("android.intent.action.GET_CONTENT");
        i.setType("image/*");
        Orkloge_settings.this.startActivityForResult(i, 1);
    }

    public void onSharedPreferenceChanged(SharedPreferences sharedPreferences,
            String key) {
    	
    }
}

