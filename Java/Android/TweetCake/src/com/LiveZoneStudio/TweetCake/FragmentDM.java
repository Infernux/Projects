package com.LiveZoneStudio.TweetCake;

import java.util.ArrayList;

import com.LiveZoneStudio.TweetCake.FragmentList.ViewHolder;

import android.graphics.Bitmap;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;

import twitter4j.DirectMessage;
import twitter4j.ResponseList;

public class FragmentDM extends FragmentTwitter{
	ArrayList<Tweet> dms = new ArrayList<Tweet>();
	ListAdapter adapter;
	
	@Override
	public View onCreateView(LayoutInflater inflater, final ViewGroup container, Bundle saved){
		View v = inflater.inflate(R.layout.listtwit, container, false);
		
		TextView t = (TextView)v.findViewById(R.id.textList);
		t.setText("Direct Messages");
		
		ListView list = (ListView)v.findViewById(R.id.listtwit);
        adapter = new ListAdapter();
        list.setAdapter(adapter);
        
        init();
		
		return v;
	}
	
	public void setParams(ResponseList<DirectMessage> msg){
		for(DirectMessage dm : msg){
			Bitmap b = TweetCakeActivity.cacheManager.getBitmap(dm.getSender());
			dms.add(new Tweet(b, dm.getText(), dm.getSender().getName(), dm.getCreatedAt().getTime(), dm.getSender(), dm.getId(), false));
		}
	}
	
	@Override
	public void update(){
		int i=0;
		for(DirectMessage dm : TweetCakeActivity.twitaccess.getDM()){
			if(dms.get(i).mId<dm.getId()){
				Bitmap b = TweetCakeActivity.cacheManager.getBitmap(dm.getSender());
				dms.add(i, new Tweet(b, dm.getText(), dm.getSender().getName(), dm.getCreatedAt().getTime(), dm.getSender(), dm.getId(), false));
				refresh();
			}else{
				break;
			}
		}
	}

	private void init(){
		DownloadTweets down = new DownloadTweets();
		down.execute();
	}
	
	@Override
	public void refresh(){
		if(isVisible()){
			getActivity().runOnUiThread(new Runnable(){
				@Override
				public void run() {
					adapter.notifyDataSetChanged();	
				}
			});
		}
	}
	
	private class ListAdapter extends BaseAdapter {
		@Override
		public int getCount() {
			return dms.size();
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
			
			ElapsedTime d = new ElapsedTime(System.currentTimeMillis()-dms.get(position).mDate);
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
			
			holder.image.setImageBitmap(dms.get(position).mAvatar);
			
			holder.tweet.setText(dms.get(position).mTweet);
			
			holder.auteur.setText(dms.get(position).mAuteur);
			
			holder.date.setText(temps);
			
			return convertView;
		}
	}
	
	private class DownloadTweets extends AsyncTask<Void, Tweet, Long> {
	     @Override
		protected Long doInBackground(Void... urls) {
		    for(twitter4j.DirectMessage dm : TweetCakeActivity.twitaccess.getDM()){
		    	Bitmap b = TweetCakeActivity.cacheManager.getBitmap(dm.getSender());
				publishProgress(new Tweet(b, dm.getText(), dm.getSender().getName(), dm.getCreatedAt().getTime(), dm.getSender(), dm.getId(), false));
		 	}
	         
	    	return null;
	     }
	     
	    @Override
	    protected void onProgressUpdate(Tweet... progress) {
	    	dms.add(progress[0]);
	    	adapter.notifyDataSetChanged();
	    }
	     
	     @Override
	     protected void onCancelled(){
	    	 
	     }

	     @Override
		protected void onPostExecute(Long result) {
	     }
	 }
}