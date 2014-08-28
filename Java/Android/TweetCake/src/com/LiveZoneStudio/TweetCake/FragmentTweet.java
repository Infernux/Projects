package com.LiveZoneStudio.TweetCake;

import java.io.IOException;

import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;

import twitter4j.User;

import android.app.Fragment;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.animation.Animation;
import android.view.animation.Animation.AnimationListener;
import android.view.animation.ScaleAnimation;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

public class FragmentTweet extends Fragment{
	TextView txt;
	ImageView img;
	String mNom, mTag, mText;
	long mTweetId;
	Bitmap mBitmap = null;
	
	Thread thread = new Thread();
	
	@Override
	public void onCreate(Bundle savedInstanceState){
		super.onCreate(savedInstanceState);
		
	}
	
	@Override
	public View onCreateView(LayoutInflater inflater, final ViewGroup container, Bundle saved){
		View v = inflater.inflate(R.layout.l_detailtweet, container, false);
		
		txt = (TextView)v.findViewById(R.id.textdetailtweet);
		txt.setText(mText);
		
		img = (ImageView)v.findViewById(R.id.imgdetailtweet);
		img.setImageBitmap(mBitmap);
		
		final Button rep = (Button)v.findViewById(R.id.boutonDetailRep);
		rep.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View v) {
				String ats = "@"+mTag+" ";
				((TweetCakeActivity)getActivity()).writeTweet(ats);
				
				Animation animation = new ScaleAnimation(1.0f, 0, 1.0f, 0, rep.getWidth()/2, rep.getHeight()/2);
				animation.setDuration(250);
				animation.setAnimationListener(new AnimationListener(){
					@Override
					public void onAnimationEnd(Animation animation) {
						animation = new ScaleAnimation(0, 1.0f, 0, 1.0f, rep.getWidth()/2, rep.getHeight()/2);
						animation.setDuration(250);
						rep.startAnimation(animation);
					}

					@Override
					public void onAnimationRepeat(Animation animation) {
					}
					
					@Override
					public void onAnimationStart(Animation animation) {
					}
				});
				rep.startAnimation(animation);
			}
		});
		
		final Button rt = (Button)v.findViewById(R.id.boutonDetailRT);
		
		rt.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View v) {
				getActivity().runOnUiThread(new Runnable(){
					@Override
					public void run() {
						Toast.makeText(getActivity(), "En cours de RT", 2000).show();
					}
				});
				TweetCakeActivity.twitaccess.retweet(mTweetId);
				Animation animation = new ScaleAnimation(1.0f, 0, 1.0f, 0, rt.getWidth()/2, rt.getHeight()/2);
				animation.setDuration(250);
				animation.setAnimationListener(new AnimationListener(){
					@Override
					public void onAnimationEnd(Animation animation) {
						animation = new ScaleAnimation(0, 1.0f, 0, 1.0f, rt.getWidth()/2, rt.getHeight()/2);
						animation.setDuration(250);
						rt.startAnimation(animation);
					}

					@Override
					public void onAnimationRepeat(Animation animation) {
					}
					
					@Override
					public void onAnimationStart(Animation animation) {
					}
				});
				rt.startAnimation(animation);
			}
		});
		
		Button favo = (Button)v.findViewById(R.id.boutonDetailFavo);
		favo.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View v) {
				new Thread(new Runnable(){
					@Override
					public void run() {
						TweetCakeActivity.twitaccess.favorite(mTweetId);
					}
				}).start();
			}
		});
		
		return v;
	}
	
	public void setParams(String tweet, User user, long tweetId){
		mNom = user.getName();
		mTweetId = tweetId;
		mTag = user.getScreenName();
		mText = tweet;
		
		isSite(tweet);
	}
	
	public void update(final String tweet, User user, long tweetId){
		mNom = user.getName();
		mTweetId = tweetId;
		mTag = user.getScreenName();
		img.setImageBitmap(null);
		txt.setText(tweet);
		
		thread.interrupt();
		
		isSite(tweet);
	}
	
	public void isSite(final String tweet){
		if(tweet.contains("http://t.co/")){
			if(thread.isAlive()==false){
				thread = new Thread(new Runnable(){
					String raw = null;
					@Override
					public void run() {
						HttpClient client = new DefaultHttpClient();
						HttpGet get = new HttpGet(getUrl(tweet));
						Log.i("adresse", getUrl(tweet));
						try {
							HttpResponse response = client.execute(get);
							raw = TwitterAccess.convertStreamToString(response.getEntity().getContent());
						} catch (ClientProtocolException e) {
							//TODO protection anti problème !
							e.printStackTrace();
						} catch (IOException e) {
							//TODO protection anti problème !
							e.printStackTrace();
						}
						
						if(raw.contains("twitpic.com")){
							client = new DefaultHttpClient();
							get = new HttpGet("http://twitpic.com/"+getUrlSrc(raw));
							try {
								HttpResponse response = client.execute(get);
								raw = TwitterAccess.convertStreamToString(response.getEntity().getContent());
							}catch (ClientProtocolException e) {
								//TODO protection anti problème !
								e.printStackTrace();
							} catch (IOException e) {
								//TODO protection anti problème !
								e.printStackTrace();
							}
							
							final Bitmap b = CacheManager.dlImage(getUrlImage(raw));
							getActivity().runOnUiThread(new Runnable(){
								@Override
								public void run() {
									img.setImageBitmap(b);
								}
							});
						}
					}
				});
				thread.start();
			}
		}
	}
	
	private String getUrl(String raw){
		int fin=0;
		
		int debut=raw.indexOf("http://t.co", fin);
		fin=raw.indexOf(" ", debut);
		
		if(fin==-1){
			fin=raw.length();
		}
		
		char[] buffer;
		
		buffer=new char[fin-debut];
		raw.getChars(debut, fin, buffer, 0);
		String url=new String(buffer);
		
		return url;
	}
	
	private String getUrlSrc(String raw){
		int fin=0;
		
		int debut=raw.indexOf("thumb", fin);
		fin=raw.indexOf("\"", debut);
		
		char[] buffer;
		
		buffer=new char[fin-debut-6-4];
		raw.getChars(debut+6, fin-4, buffer, 0);
		String url=new String(buffer);
		
		return url;
	}
	
	private String getUrlImage(String raw){
		int fin=0;
		
		int debut=raw.indexOf("full\"", fin);
		debut=raw.indexOf("<img src=\"http", debut);
		fin=raw.indexOf("\" ", debut);
		
		char[] buffer;
		
		buffer=new char[fin-debut-10];
		raw.getChars(debut+10, fin, buffer, 0);
		String url=new String(buffer);
		
		return url;
	}
}