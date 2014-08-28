package com.LiveZoneStudio.TweetCake;

import android.app.Fragment;
import android.os.AsyncTask;
import android.view.MenuItem;
import android.view.animation.Animation;

public abstract class FragmentTwitter extends Fragment{
	
	Thread thread;
	AsyncTask<Void, Tweet, Void> task;
	
	public void update(){
	}
	
	public void refresh(){
	}
	
	@Override
	public void onHiddenChanged(boolean hidden){
		super.onHiddenChanged(hidden);
		
		if(hidden==true){
			if(task!=null){
				task.cancel(true);
			}
		}
	}
	
	@Override
	public void onStart(){
		super.onStart();
		
		new Thread(new Runnable(){
			@Override
			public void run() {
				refresh();
			}
		}).start();
	}

	public void update(MenuItem item, Animation anim) {
		
	}
}
