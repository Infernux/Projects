package com.LiveZoneStudio.TweetCake;

import twitter4j.User;
import android.graphics.Bitmap;

public class Tweet {
	Bitmap mAvatar;
	String mTweet, mAuteur;
	User mUser;
	long mId, mDate;
	boolean mRT=false;
	
	public Tweet(Bitmap avatar, String tweet, String auteur, long date, User user, long id, boolean RT){
		mAvatar = avatar;
		mTweet = tweet;
		mAuteur = auteur;
		mDate = date;
		mUser = user;
		mId = id;
		mRT = RT;
	}
}