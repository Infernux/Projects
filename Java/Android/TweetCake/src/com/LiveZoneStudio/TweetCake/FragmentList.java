package com.LiveZoneStudio.TweetCake;

import java.util.ArrayList;
import android.graphics.Bitmap;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.view.animation.Animation;
import android.widget.AbsListView;
import android.widget.AdapterView;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;

import twitter4j.Paging;
import twitter4j.ResponseList;

public class FragmentList extends FragmentTwitter{
	ArrayList<Tweet> tweets = new ArrayList<Tweet>();
	ListAdapter adapter;
	
	Paging old, nouveau;
	
	int MAX_TWEETS = 100;

	@Override
	public void onCreate(Bundle savedInstanceState){
		super.onCreate(savedInstanceState);
		
		if(tweets.size()==0){
			init();
		}
		thread = new Thread();
		task = null;
		nouveau = new Paging();
		old = new Paging();
		nouveau.setCount(20);
		old.setCount(20);
	}
	
	private void checkTweetSize(){
		if(tweets.size()>MAX_TWEETS){
			for(int i=0; i<20; ++i){
				tweets.remove(tweets.size()-1);
			}
			//TweetCakeActivity.twitaccess.restorePaging();
		}
	}
	
	@Override
	public void update(MenuItem item, Animation anim){
		TweetCakeActivity.twitaccess.setPaging(nouveau);
		
		DownloadTweets down = new DownloadTweets();
		down.setItems(item, anim);
		down.execute("1");
	}
	
	public void init(){
		DownloadTweets down = new DownloadTweets();
		down.execute("0");
	}
	
	/*public void updateOldTweet(ResponseList<Status> status){
		
	}*/
	
	/*public void refresh(){
		if(isVisible()){
			getActivity().runOnUiThread(new Runnable(){
				@Override
				public void run() {
					adapter.notifyDataSetChanged();
				}
			});
		}
	}*/
	
	@Override
	public View onCreateView(LayoutInflater inflater, final ViewGroup container, Bundle saved){
		View v = inflater.inflate(R.layout.listtwit, container, false);
		
		ListView list = (ListView)v.findViewById(R.id.listtwit);
        adapter = new ListAdapter();
        list.setAdapter(adapter);
        
        list.setOnItemClickListener(new AdapterView.OnItemClickListener(){
			@Override
			public void onItemClick(AdapterView<?> arg0, View arg1, int pos,
					long arg3) {
				((TweetCakeActivity)getActivity()).onTweetSelected(tweets.get(pos).mUser, tweets.get(pos).mTweet, tweets.get(pos).mId);
			}
		});  
        
        list.setOnScrollListener(new AbsListView.OnScrollListener() {
			@Override
			public void onScrollStateChanged(AbsListView view, int scrollState) {				
				if(scrollState==0 && view.getLastVisiblePosition()==tweets.size()-1){
					if(task!=null){
						return;
					}
					
					task = new AsyncTask<Void, Tweet, Void>() {

						@Override
						protected Void doInBackground(Void... params) {
							TweetCakeActivity.twitaccess.login();
							old.setMaxId(tweets.get(tweets.size()-1).mId-1);
							TweetCakeActivity.twitaccess.setPaging(old);
							for(twitter4j.Status tweet : TweetCakeActivity.twitaccess.getTweets()){
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
							return null;
						}
						
						@Override
						protected void onProgressUpdate(Tweet... progress) {
							tweets.add(progress[0]);
					    	adapter.notifyDataSetChanged();
					    }
						
						@Override
						protected void onPostExecute(Void v){
							task=null;
						}
			        };
			        
			        task.execute();
				}
			}
			
			@Override
			public void onScroll(AbsListView view, int firstVisibleItem,
					int visibleItemCount, int totalItemCount) {}
		});

		return v;
	}
	
	private class ListAdapter extends BaseAdapter {
		int flag_more=-1;
		
		@Override
		public int getCount() {
			return tweets.size();
		}
		
		public void setMore(int line){
			flag_more=line;
		}
		
		public void noMore(){
			flag_more=-1;
		}
		
		public int getMore(){
			return flag_more;
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
				holder.isRT = (ImageView) convertView.findViewById(R.id.rttwit);
				convertView.setTag(holder);
			}else{
				holder = (ViewHolder)convertView.getTag();
			}
			
			if(position==flag_more){
				holder.tweet.setText("DL more ?");
				holder.image.setImageBitmap(null);
				holder.auteur.setText(null);
				holder.date.setText(null);
				holder.isRT.setImageBitmap(null);
				
				convertView.setOnClickListener(new View.OnClickListener() {
					@Override
					public void onClick(View v) {
						if(task!=null){
							return;
						}
						
						task = new AsyncTask<Void, Tweet, Void>() {

							@Override
							protected Void doInBackground(Void... params) {
								TweetCakeActivity.twitaccess.login();
								//Creation d'un paging pour récupérer les tweets dont on a besoin
								Paging paging = new Paging();
								paging.setCount(20);
								paging.setMaxId(tweets.get(flag_more).mId-1);
								paging.setSinceId(tweets.get(flag_more-1).mId+1);
								TweetCakeActivity.twitaccess.setPaging(paging);
								//suppression du flagmore dans la liste des tweets
								tweets.remove(flag_more);
								
								ResponseList<twitter4j.Status> s = TweetCakeActivity.twitaccess.getTweets();
								for(int i=0; i<20; ++i){
									twitter4j.Status tweet = s.get(i);
									if(tweet.getId()>tweets.get(flag_more).mId){
										Bitmap b=null;
										if(tweet.isRetweet()){
											tweet = tweet.getRetweetedStatus();
											b = TweetCakeActivity.cacheManager.getBitmap(tweet.getUser());
											publishProgress(new Tweet(b , tweet.getText(), tweet.getUser().getName(), tweet.getCreatedAt().getTime(), tweet.getUser(), tweet.getId(), true));
										}else{
											b = TweetCakeActivity.cacheManager.getBitmap(tweet.getUser());
											publishProgress(new Tweet(b , tweet.getText(), tweet.getUser().getName(), tweet.getCreatedAt().getTime(), tweet.getUser(), tweet.getId(), false));
										}
									}else{
										adapter.noMore();
										break;
									}
									//adapter.setMore(flag_more+20);
								}
								return null;
							}
							
							@Override
							protected void onProgressUpdate(Tweet... progress) {
								tweets.add(progress[0]);
						    	adapter.notifyDataSetChanged();
						    }
							
							@Override
							protected void onPostExecute(Void v){
								task=null;
							}
				        };
				        
				        task.execute();
					}
				});
			}else{
				ElapsedTime d = new ElapsedTime(System.currentTimeMillis()-tweets.get(position).mDate);
				String temps = null;
				//Calcul du temps pour l'affichage
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
				if(tweets.get(position).mRT){
					holder.isRT.setImageResource(R.drawable.retweet);
				}else{
					holder.isRT.setImageBitmap(null);
				}
			}
			
			
			return convertView;
		}
	}
	
	static class ViewHolder {
	  TextView tweet,auteur,date;
	  ImageView image, isRT;
	}
	
	private class DownloadTweets extends AsyncTask<String, Tweet, Long> {
		Animation m_Anim;
		MenuItem m_Item;
		
	    @Override
		protected Long doInBackground(String... types) {
	    	synchronized(tweets){
	    		switch(Integer.valueOf(types[0])){
	    		/** Initialisation */
		    		case 0:
		    			int i;
		    			ResponseList<twitter4j.Status> s = TweetCakeActivity.twitaccess.getTweets();
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
		    			s = TweetCakeActivity.twitaccess.getTweets();
		    			for(i=s.size()-1; i>=0; --i){
		    				twitter4j.Status tweet = s.get(i);
		    				if(tweet.getId()>tweets.get(0).mId){
		    					//TODO A remettre à size()-1 
		    					if(i==(s.size()-1)){		    						
		    						adapter.setMore(s.size()-1);
		    					}
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
		    			if(adapter.getMore()!=-1){
		    				publishProgress(null);
		    			}
		    			return (long) 1;
	    		}
	    	}
	         
	    	return null;
	     }
	    
	    @Override
	    protected void onProgressUpdate(Tweet... progress) {
	    	super.onProgressUpdate(progress);
	    	if(progress==null){
	    		//si flag_more, on ajoute un faux rang
	    		tweets.add(19, new Tweet(null , null, null, 10, null, 10, false));
	    	}else{
	    		//sinon on ajoute le tweet normalement
	    		tweets.add(0, progress[0]);
	    	}
	    	adapter.notifyDataSetChanged();
	    }
	     
	     @Override
	     protected void onCancelled(){
	    	 
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
