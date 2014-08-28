package com.LiveZoneStudio.TweetCake;

import twitter4j.User;
import android.app.Fragment;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

public class FragmentUser extends Fragment{
	ImageView img;
	TextView nom, nbTweet, nbAbo, nbFollower;
	Bitmap b;
	String m_Nom;
	int m_Nbtweet, m_Nbabo, m_Nbfollower;
	
	@Override
	public View onCreateView(LayoutInflater inflater, final ViewGroup container, Bundle saved){
		View v = inflater.inflate(R.layout.l_user, container, false);
		img = (ImageView)v.findViewById(R.id.imgUser);
		nom = (TextView)v.findViewById(R.id.nomUser);
		nbTweet = (TextView)v.findViewById(R.id.nbTweetsUser);
		nbAbo = (TextView)v.findViewById(R.id.nbAboUser);
		nbFollower = (TextView)v.findViewById(R.id.nbFollowerUser);
		img.setImageBitmap(b);
		nom.setText(m_Nom);
		nbTweet.setText(String.valueOf(m_Nbtweet));
		nbAbo.setText(String.valueOf(m_Nbabo));
		nbFollower.setText(String.valueOf(m_Nbfollower));
		
		return v;
	}
	
	public void initiate(User user){
		b = TweetCakeActivity.cacheManager.getBitmap(user);
		m_Nom = user.getName();
		m_Nbtweet = user.getStatusesCount();
		m_Nbabo = user.getFriendsCount();
		m_Nbfollower = user.getFollowersCount();
	}
	
	public void setUser(User user){
		b = TweetCakeActivity.cacheManager.getBitmap(user);
		img.setImageBitmap(b);
		nom.setText(user.getName());
		nbTweet.setText(String.valueOf(user.getStatusesCount()));
		nbAbo.setText(String.valueOf(user.getFriendsCount()));
		nbFollower.setText(String.valueOf(user.getFollowersCount()));
	}
}
