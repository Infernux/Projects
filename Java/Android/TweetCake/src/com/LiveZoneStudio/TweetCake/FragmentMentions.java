package com.LiveZoneStudio.TweetCake;

import java.util.ArrayList;

import com.LiveZoneStudio.TweetCake.FragmentList.ViewHolder;

import twitter4j.ResponseList;
import android.graphics.Bitmap;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.view.animation.Animation;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;

public class FragmentMentions extends FragmentTwitter{
	ArrayList<Tweet> tweets = new ArrayList<Tweet>();
	ListAdapter adapter;
	
	@Override
	public void onCreate(Bundle savedInstanceState){
		super.onCreate(savedInstanceState);
	}
	
	@Override
	public View onCreateView(LayoutInflater inflater, final ViewGroup container, Bundle saved){
		View v = inflater.inflate(R.layout.listtwit, container, false);
		
		TextView txt = (TextView)v.findViewById(R.id.textList);
		txt.setText("Mentions");
		
		ListView list = (ListView)v.findViewById(R.id.listtwit);
        adapter = new ListAdapter();
        list.setAdapter(adapter);
        
        if(tweets.size()==0){
        	init();
        }
		
		return v;
	}
	
	@Override
	public void update(MenuItem item, Animation anim){
		DownloadTweets down = new DownloadTweets();
		down.setItems(item, anim);
		down.execute("1");
	}
	
	public void init(){
		DownloadTweets down = new DownloadTweets();
		down.execute("0");
		//refresh();
	}
	
	/*@Override
	public void refresh(){		
		if(isVisible()){
			getActivity().runOnUiThread(new Runnable(){
				@Override
				public void run() {
					adapter.notifyDataSetChanged();	
				}
			});
		}
	}*/
	
	private class ListAdapter extends BaseAdapter {
		@Override
		public int getCount() {
			return tweets.size();
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
				LayoutInflater li = getActivity().getLayoutInflater();
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
			
			ElapsedTime d = new ElapsedTime(System.currentTimeMillis()-tweets.get(position).mDate);
			String temps = null;
			if(d.getMois()!=0){
				temps = String.valueOf(d.getMois())+"m";
			}else if(d.getJours()!=0){
				temps = String.valueOf(d.getJours())+"j";
			}else if(d.getHeures()!=0){
				temps = String.valueOf(d.getHeures())+"h";
			}else if(d.getMinutes()!=0){
				temps = String.valueOf(d.getMinutes())+"min";
			}else{
				temps = String.valueOf(d.getSecondes())+"s";
			}
			
			holder.image.setImageBitmap(tweets.get(position).mAvatar);
			
			holder.tweet.setText(tweets.get(position).mTweet);
			
			holder.auteur.setText(tweets.get(position).mAuteur);
			
			holder.date.setText(temps);
			
			return convertView;
		}
	}
	
	private class DownloadTweets extends AsyncTask<String, Tweet, Long> {
		Animation m_Anim;
		MenuItem m_Item;
	    
		@Override
		protected Long doInBackground(String... types) {
	    	 switch(Integer.valueOf(types[0])){
	    		/** Initialisation */
	    		case 0:
	    			int i;
	    			ResponseList<twitter4j.Status> s = TweetCakeActivity.twitaccess.getMentions();
	    			for(i=s.size()-1; i>=0; --i){
	    				twitter4j.Status tweet = s.get(i);
	    				Bitmap b=null;
						if(tweet.isRetweet()){
							tweet = tweet.getRetweetedStatus();
							b = TweetCakeActivity.cacheManager.getBitmap(tweet.getUser());
							publishProgress(new Tweet(b , tweet.getText(), tweet.getUser().getName(), tweet.getCreatedAt().getTime(), tweet.getUser(), tweet.getId(), true));
						}else{
							b = TweetCakeActivity.cacheManager.getBitmap(tweet.getUser());
							publishProgress(new Tweet(b , tweet.getText(), tweet.getUser().getName(), tweet.getCreatedAt().getTime(), tweet.getUser(), tweet.getId(), false));
						}
	    	 		}
	    			break;
	    			
	    		case 1:
	    			//checkTweetSize();
	    			s = TweetCakeActivity.twitaccess.getMentions();
	    			for(i=s.size()-1; i>=0; --i){
	    				twitter4j.Status tweet = s.get(i);
	    				if(tweet.getId()>tweets.get(0).mId){
	    					Bitmap b=null;
	    					if(tweet.isRetweet()){
								tweet = tweet.getRetweetedStatus();
								b = TweetCakeActivity.cacheManager.getBitmap(tweet.getUser());
								publishProgress(new Tweet(b , tweet.getText(), tweet.getUser().getName(), tweet.getCreatedAt().getTime(), tweet.getUser(), s.get(0).getId(), true));
							}else{
								b = TweetCakeActivity.cacheManager.getBitmap(tweet.getUser());
								publishProgress(new Tweet(b , tweet.getText(), tweet.getUser().getName(), tweet.getCreatedAt().getTime(), tweet.getUser(), tweet.getId(), false));
							}
	    				}else{
	    					continue;
	    				}
	    			}
	    			return (long) 1;
	    	}
	    	return null;
	     }
	     
	     @Override
	     protected void onProgressUpdate(Tweet... progress) {
	    	 super.onProgressUpdate(progress);
	    	 tweets.add(0, progress[0]);
	    	 adapter.notifyDataSetChanged();
	     }
	     
	    @Override
		protected void onPostExecute(Long result) {
		   	if(result!=null){
		   		m_Anim.cancel();
				m_Item.setActionView(null);
		   	}
		}
		     
		public void setItems(MenuItem item, Animation anim){
		   	 m_Anim = anim;
		   	 m_Item = item;
		}
	 }
}