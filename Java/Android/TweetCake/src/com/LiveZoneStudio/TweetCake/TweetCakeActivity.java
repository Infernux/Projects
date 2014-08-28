package com.LiveZoneStudio.TweetCake;

import java.util.ArrayList;
import java.util.TimeZone;

import twitter4j.ResponseList;
import twitter4j.User;
import twitter4j.UserList;
import android.app.ActionBar;
import android.app.ActionBar.Tab;
import android.app.Activity;
import android.app.Dialog;
import android.app.Fragment;
import android.app.FragmentManager;
import android.app.FragmentTransaction;
import android.content.Context;
import android.content.DialogInterface;
import android.content.DialogInterface.OnDismissListener;
import android.content.Intent;
import android.content.res.Configuration;
import android.os.Bundle;
import android.os.SystemClock;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.Gravity;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewGroup.LayoutParams;
import android.view.Window;
import android.view.WindowManager;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ArrayAdapter;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ListPopupWindow;
import android.widget.TextView;

public class TweetCakeActivity extends Activity {
	static TwitterAccess twitaccess;
	static CacheManager cacheManager;
	static int saving;
	
	boolean tablette=true;
	
	FragmentManager fm;
	
	ArrayList<FragmentTwitter> fragments = new ArrayList<FragmentTwitter>();
    
	Thread thread;
	
	ImageView iv = null;
	
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        twitaccess = new TwitterAccess(this);
        cacheManager = new CacheManager(this);
        TimeZone timeZone = TimeZone.getDefault();
        saving = timeZone.getDSTSavings();
        
        fm = getFragmentManager();
        
        final Object l = new Object();
        
        thread = new Thread(new Runnable(){
			@Override
			public void run() {
				synchronized(l){
					twitaccess.login();
					l.notify();
				}
			}
        });
        thread.start();
        
	    try {
	      	synchronized(l){
	      		l.wait();
	       	}
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
        
        setContentView(R.layout.main);
        
        if(findViewById(R.id.modifLayout2)==null){
        	tablette=false;
        }
        
        final FragmentList timeline = new FragmentList();
        final FragmentMentions mention = new FragmentMentions();
        final FragmentDM dm = new FragmentDM();
        fragments.add(timeline);
        fragments.add(mention);
        fragments.add(dm);
        
        ActionBar actionBar = this.getActionBar();
        
        actionBar.setNavigationMode(ActionBar.NAVIGATION_MODE_TABS);
        
        Tab tab = actionBar.newTab().setText("TimeLine").setTabListener(new TabListener(this, "TimeLine"));
        actionBar.addTab(tab);
        if(!tablette){
        	tab = actionBar.newTab().setText("Mentions").setTabListener(new TabListener(this, "Mentions"));
            actionBar.addTab(tab);
        }
        tab = actionBar.newTab().setText("Direct Messages").setTabListener(new TabListener(this, "DM"));
        actionBar.addTab(tab);
    }
    
    @Override
    public void onAttachFragment(Fragment fragment){
    	super.onAttachFragment(fragment);
    	
    	if(twitaccess == null){
    		twitaccess = new TwitterAccess(this);
    		thread = new Thread(new Runnable(){
    			@Override
    			public void run() {
    				twitaccess.login();
    			}
            });
            thread.start();
            
            while(thread.isAlive()){
            	SystemClock.sleep(100);
            }
    	}
    }
    
    @Override
    public void onBackPressed(){
    	super.onBackPressed();
    	
    	ActionBar actionBar = getActionBar();
		actionBar.setTitle("TweetCake");
		actionBar.setDisplayHomeAsUpEnabled(false);
		fm.popBackStack();
    }
    
    @Override
    public void onConfigurationChanged(Configuration c){
    	super.onConfigurationChanged(c);
    }
    
    @Override
    public void onPause(){
    	super.onPause();
    	
    	if(thread.isAlive()){
    		thread.interrupt();
    	}
    }
    
    @Override
    public void onStop(){
    	super.onStop();
    	
    	cacheManager.purgeFile();
    }
    
    public void onTweetSelected(User user, String tweet, long id) 
    {
    	ActionBar actionBar = getActionBar();
    	actionBar.setDisplayHomeAsUpEnabled(true);
    	actionBar.setTitle(user.getName());
    	
    	FragmentUser viewer = (FragmentUser) fm.findFragmentByTag("user");
    	FragmentTweet tweetDetail = (FragmentTweet) fm.findFragmentByTag("detail");
    	
    	if(viewer==null){
    		FragmentTransaction ft = fm.beginTransaction();
    		viewer = new FragmentUser();
    		tweetDetail = new FragmentTweet();
    		if(tablette){
		    	LinearLayout fl1 = (LinearLayout)findViewById(R.id.modifLayout2);
		    	fl1.setLayoutParams(new LinearLayout.LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT));
		    	
		    	LinearLayout fl2 = (LinearLayout)findViewById(R.id.modifLayout3);
		    	fl2.setLayoutParams(new LinearLayout.LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT));
		    	fl2.setVisibility(View.VISIBLE);
		        
		        viewer.initiate(user);
	            tweetDetail.setParams(tweet, user, id);
	            
	            ft.replace(R.id.modifLayout2, viewer, "user");
		    	ft.replace(R.id.modifLayout3, tweetDetail, "detail");
    		}else{
    			LinearLayout fl1 = (LinearLayout)findViewById(R.id.modifLayout);
		    	fl1.setLayoutParams(new LinearLayout.LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT));
		        fl1.setVisibility(View.VISIBLE);
		        fl1.invalidate();
		    	
		    	LinearLayout fl2 = (LinearLayout)findViewById(R.id.modifLayout1);
		    	fl2.setLayoutParams(new LinearLayout.LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT));
		    	fl2.setVisibility(View.VISIBLE);
		    	
    			viewer.initiate(user);
	            tweetDetail.setParams(tweet, user, id);
    			
    			ft.replace(R.id.modifLayout, viewer, "user");
		    	ft.replace(R.id.modifLayout1, tweetDetail, "detail");
    		}
    		
    		fm.popBackStack();
	    	
	    	ft.addToBackStack(null);
	        
	        ft.commit();
    	}else{
    		viewer.setUser(user);
    		tweetDetail.update(tweet, user, id);
    	}
    }
    
    @Override
    public boolean onOptionsItemSelected(MenuItem item){
    	switch(item.getItemId()){
    		case android.R.id.home:
    			ActionBar actionBar = getActionBar();
    			actionBar.setTitle("TweetCake");
    			actionBar.setDisplayHomeAsUpEnabled(false);
    			fm.popBackStack();
    			return true;
    	}
    	return true;
    }
    
    @Override
    public boolean onCreateOptionsMenu(final Menu menu) {    	
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.layout.action_bar, menu);
        
		final Animation anim = AnimationUtils.loadAnimation(TweetCakeActivity.this, R.drawable.reload_anim);
        
        menu.findItem(R.id.menu_tweet).setOnMenuItemClickListener(new MenuItem.OnMenuItemClickListener() {
			@Override
			public boolean onMenuItemClick(MenuItem item) {
				writeTweet("");
				return false;
			}
		});
        
        menu.findItem(R.id.menu_refresh).setOnMenuItemClickListener(new MenuItem.OnMenuItemClickListener() {
			@Override
			public boolean onMenuItemClick(final MenuItem item) {
				item.setActionView(R.layout.reload);
				iv = (ImageView)findViewById(R.id.aaaa);
				
				iv.startAnimation(anim);
				
				if(!thread.isAlive()){
					thread = new Thread(new Runnable(){
						@Override
						public void run() {
							twitaccess.login();
							//twitaccess.restorePaging();
							reload(item, anim);
						}
			        });
					thread.start();
				}
				return false;
			}
		});
        return true;
    }
    
    public void reload(MenuItem item, Animation anim){
    	for(FragmentTwitter fragment : fragments){
    		if(fragment.isVisible()){
    			fragment.update(item, anim);
    		}
    	}
    }
    
    void writeTweet(String ats) {
    	Intent intent = new Intent(this, TweetActivity.class);
		intent.putExtra("ats", ats);
		startActivity(intent);
	}
    
    public class TabListener implements ActionBar.TabListener {
        private Fragment mFragment;
        private String mTag;
        
        public TabListener(Activity activity, String tag) {
        	mTag = tag;
        }

        @Override
		public void onTabSelected(Tab tab, FragmentTransaction ft) {
        	fm.popBackStack();
        	
        	ActionBar actionBar = getActionBar();
			actionBar.setTitle("TweetCake");
			actionBar.setDisplayHomeAsUpEnabled(false);
        	
        	if(mTag.contains("TimeLine")){
        		final FragmentList timeline = (FragmentList)fragments.get(0);
        		ft.replace(R.id.modifLayout, timeline, "timeline");
        		if(tablette){
        			FragmentMentions mention = (FragmentMentions)fm.findFragmentByTag("mentions"); 
                    if(mention==null){
                    	mention = (FragmentMentions)fragments.get(1);
                    	ft.replace(R.id.modifLayout2, mention, "mentions");
                    }
        		}
        	}else if(mTag.contains("DM")){
        		final FragmentDM dm = (FragmentDM)fragments.get(2);
                
                ft.replace(R.id.modifLayout, dm, "dm");
        	}else{
        		final FragmentMentions mention = (FragmentMentions)fragments.get(1);
                
                if(fm.findFragmentByTag("mentions")==null){
                	ft.replace(R.id.modifLayout, mention, "mentions");
                }
        	}
        	
        }

        @Override
		public void onTabUnselected(Tab tab, FragmentTransaction ft) {
        }

        @Override
		public void onTabReselected(Tab tab, FragmentTransaction ft) {
        	fm.popBackStack();
        	
        	ActionBar actionBar = getActionBar();
			actionBar.setTitle("TweetCake");
			actionBar.setDisplayHomeAsUpEnabled(false);
        }
    }
    
    /*private class ListAdapter extends BaseAdapter {
		@Override
		public int getCount() {
			//return tweets.size();
			return 2;
		}

		@Override
		public Object getItem(int position) {
			return position;
		}

		@Override
		public long getItemId(int position) {
			return position;
		}

		@Override
		public View getView(int position, View convertView, ViewGroup parent) {
			ViewHolder holder;
			if(convertView == null){
				LayoutInflater li = getLayoutInflater();
				convertView = li.inflate(R.layout.rowtwit, null);
				holder = new ViewHolder();
				holder.tweet = (TextView) convertView.findViewById(R.id.texttwit);
				holder.auteur = (TextView) convertView.findViewById(R.id.auteurtwit);
				holder.date = (TextView) convertView.findViewById(R.id.datetwit);
				holder.image = (ImageView) convertView.findViewById(R.id.imagetwit);
				convertView.setTag(holder);
				//myView = li.inflate(R.layout.rowtwit, null);
			}else{
				holder = (ViewHolder)convertView.getTag();
			}
			
			TextView t = new TextView(parent.getContext());
			t.setText("test");
			
			//return convertView;
			return t;
		}
	}*/
}