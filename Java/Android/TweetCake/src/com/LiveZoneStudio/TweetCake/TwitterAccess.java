package com.LiveZoneStudio.TweetCake;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;

import twitter4j.DirectMessage;
import twitter4j.IDs;
import twitter4j.Paging;
import twitter4j.ResponseList;
import twitter4j.Status;
import twitter4j.Twitter;
import twitter4j.TwitterException;
import twitter4j.TwitterFactory;
import twitter4j.User;
import twitter4j.UserList;
import twitter4j.auth.AccessToken;
import twitter4j.auth.RequestToken;


import android.content.Context;
import android.content.SharedPreferences;
import android.os.SystemClock;
import android.util.Log;
import android.widget.Toast;

public class TwitterAccess {
	private Context context;
	
	protected String CONSUMER_KEY = "bF1YqFHl2f5U6KLewCOA";
	private String CONSUMER_SECRET = "f6gdnnbOBwaEAXaMahVWEo7E8aM2OUOoN6M6ooQP7A";
	
	private AccessToken accessToken; 
	private RequestToken requestToken;
	
	private Twitter twitter;
	private Paging page;
	
	public TwitterAccess(Context cont){
		context=cont;
		System.setProperty("http.keepAlive", "false");
		page = new Paging();
		page.setPage(1);
		page.setCount(20);
	}
	
	private void toastError(){
		((TweetCakeActivity) context).runOnUiThread(new Runnable(){
			@Override
			public void run() {
				Toast.makeText(context, context.getResources().getString(R.string.erreurconn), 1000).show();
			}
		});
    }
	
	public ResponseList<DirectMessage> getDM(){
		try {
			int pos=0;
			ResponseList<DirectMessage> retour = twitter.getSentDirectMessages();
			for(DirectMessage dm : twitter.getDirectMessages()){
				while(dm.getCreatedAt().before(retour.get(pos).getCreatedAt())){
					if((pos+1)<retour.size()){
						++pos;
					}else{
						return retour;
					}
				}
				if(pos==0 && dm.getCreatedAt().getTime()==retour.get(0).getCreatedAt().getTime()){
					continue;
				}
				retour.add(pos, dm);
			}
			return retour;
		} catch (TwitterException e) {
			toastError();
			e.printStackTrace();
		}
		return null;
	}
	
	public void favorite(long id){
		try {
			twitter.createFavorite(id);
		} catch (TwitterException e) {
			toastError();
			e.printStackTrace();
		}
	}
	
	public ResponseList<Status> getTweets(){
		try {
			while(twitter==null){
				SystemClock.sleep(100);
			}
			return twitter.getHomeTimeline(page);
		} catch (TwitterException e) {
			toastError();
			e.printStackTrace();
		}
		return null;
	}
	
	public ResponseList<Status> getMentions(){
		try {
			return twitter.getMentions();
		} catch (TwitterException e) {
			toastError();
			e.printStackTrace();
		}
		
		return null;
	}
	
	public void setPaging(Paging paging){
		page = paging;
	}
	
	public void setStatus(final String status){
		new Thread(new Runnable(){
			@Override
			public void run() {
				try {
					twitter.updateStatus(status);
				} catch (TwitterException e) {
					toastError();
					e.printStackTrace();
				}	
			}
		}).start();
	}
	
	public ArrayList<String> getFriends(){
		try{
			ArrayList<String> s = new ArrayList<String>();
			for(User user : twitter.lookupUsers(twitter.getFriendsIDs(twitter.getId(), -1L).getIDs())){
				Log.i("user", user.getScreenName());
				s.add(user.getScreenName());
			}
			return s;
		}catch (IllegalStateException e){
			e.printStackTrace();
		}catch (TwitterException e){
			e.printStackTrace();
		}
		return null;
	}
	
	public void retweet(final long id){
		new Thread(new Runnable(){
			@Override
			public void run() {
				try {
					twitter.retweetStatus(id);
				} catch (TwitterException e) {
					toastError();
					e.printStackTrace();
				}
			}
		}).start();
	}
	
	public void login(){
		twitter = new TwitterFactory().getInstance();
		twitter.setOAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET);
		
		checkForSavedLogin();
		
		if(accessToken==null){
			try {
				requestToken = twitter.getOAuthRequestToken();
			} catch (TwitterException e1) {
				toastError();
				e1.printStackTrace();
			}
			
			//Login
			
			List<NameValuePair> vars = new ArrayList<NameValuePair>(3);
			vars.add(new BasicNameValuePair("oauth_token", requestToken.getToken()));
			vars.add(new BasicNameValuePair("session[username_or_email]", "user"));
			vars.add(new BasicNameValuePair("session[password]", "password"));
			
			HttpClient client = new DefaultHttpClient();
	        HttpPost httppost = new HttpPost("https://api.twitter.com/oauth/authorize");
	        
	        try {
				httppost.setEntity(new UrlEncodedFormEntity(vars));
			} catch (UnsupportedEncodingException e) {
				e.printStackTrace();
			}
	        
	        String pin = null;
	        
	        try {
				HttpResponse response = client.execute(httppost);
				pin = getPin(convertStreamToString(response.getEntity().getContent()));
			} catch (ClientProtocolException e) {
				toastError();
				e.printStackTrace();
			} catch (IOException e) {
				e.printStackTrace();
			}
	        
	        log(pin, accessToken, requestToken);
		}else{
			Log.i("stored", "incrediblu");
		}
	}
	
	private String getPin(String raw){
		int fin=0;
		
		int debut=raw.indexOf("<code>", fin);
		fin=raw.indexOf("</code>", debut);
		
		char[] buffer;
		
		buffer=new char[fin-debut-6];
		raw.getChars(debut+6, fin, buffer, 0);
		String pin=new String(buffer);
		
		return pin;
	}
	
	public static String convertStreamToString(InputStream is) {
        BufferedReader reader = new BufferedReader(new InputStreamReader(is));
        StringBuilder sb = new StringBuilder();

        String line = null;
        try {
                while ((line = reader.readLine()) != null) {
                        sb.append(line);
                }
        } catch (IOException e) {
                e.printStackTrace();
        } finally {
                try {
                        is.close();
                } catch (IOException e) {
                        e.printStackTrace();
                }
        }

        return sb.toString();
	}
	
	private void log(String pin, AccessToken accessToken, RequestToken requestToken){
		try{  
           if(pin.length() > 0){
             accessToken = twitter.getOAuthAccessToken(requestToken, pin);
           }else{
             accessToken = twitter.getOAuthAccessToken();
           }
        } catch (TwitterException te) {
          if(401 == te.getStatusCode()){
            System.out.println("Unable to get the access token.");
          }else{
            te.printStackTrace();
          }
        }
        
        try {
			System.out.println(twitter.verifyCredentials().getId());
		} catch (TwitterException e) {
			toastError();
			e.printStackTrace();
		}
	    System.out.println("token : " + accessToken.getToken());
	    System.out.println("tokenSecret : " + accessToken.getTokenSecret());
	    storeAccessToken(accessToken);
	    //twitter.verifyCredentials().getId() ,
	}
	
	private AccessToken getAccessToken() {
		SharedPreferences settings = context.getSharedPreferences("token", Context.MODE_PRIVATE);
		String token = settings.getString("accessTokenToken", "");
		String tokenSecret = settings.getString("accessTokenSecret", "");
		if (token!=null && tokenSecret!=null && !"".equals(tokenSecret) && !"".equals(token)){
			return new AccessToken(token, tokenSecret);
		}
		return null;
	}
	
	private void storeAccessToken(AccessToken a) {
		SharedPreferences settings = context.getSharedPreferences("token", Context.MODE_PRIVATE);
		SharedPreferences.Editor editor = settings.edit();
		editor.putString("accessTokenToken", a.getToken());
		editor.putString("accessTokenSecret", a.getTokenSecret());
		editor.commit();
	}
	
	private void checkForSavedLogin() {
		// Get Access Token and persist it
		accessToken = getAccessToken();
		if (accessToken==null) return;	//if there are no credentials stored then return to usual activity

		// initialize Twitter4J
		twitter.setOAuthAccessToken(accessToken);
	}
}
