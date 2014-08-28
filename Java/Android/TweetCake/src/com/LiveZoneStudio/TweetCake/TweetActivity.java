package com.LiveZoneStudio.TweetCake;

import java.util.ArrayList;

import twitter4j.ResponseList;
import twitter4j.UserList;
import android.app.Activity;
import android.content.res.Configuration;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.View;
import android.view.WindowManager;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListPopupWindow;
import android.widget.MultiAutoCompleteTextView;
import android.widget.PopupWindow;

public class TweetActivity extends Activity{
	ArrayList<String> tab = new ArrayList<String>();
	@Override
	public void onCreate(Bundle savedInstanceState){
		super.onCreate(savedInstanceState);
		
		final String ats = getIntent().getStringExtra("ats");
		
		new Thread(new Runnable(){
			@Override
			public void run() {
				synchronized(ats){
					tab = TweetCakeActivity.twitaccess.getFriends();
					ats.notify();
				}
			}
		}).start();
		
		try {
	      	synchronized(ats){
	      		ats.wait();
	       	}
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
				
		setContentView(R.layout.popuptweet);       
        
		final ArrayAdapter<String> adapter = new ArrayAdapter<String>(this, android.R.layout.simple_dropdown_item_1line, tab);
		
        final MultiAutoCompleteTextView text = (MultiAutoCompleteTextView)findViewById(R.id.tweetText);
        text.setText(ats);
        text.setAdapter(adapter);
        text.setTokenizer(new MultiAutoCompleteTextView.Tokenizer() {
			
			@Override
			public CharSequence terminateToken(CharSequence text) {
				return text+" ";
			}
			
			@Override
			public int findTokenStart(CharSequence text, int cursor){
				int i = cursor;
                while (i > 0 && text.charAt(i - 1) != '@')
                        i--;
                /*while (i < cursor && text.charAt(i) == ' ')
                        i++;*/
                return i;
			}
			
			@Override
			public int findTokenEnd(CharSequence text, int cursor) {
				int i = cursor;
                int len = text.length();
                while (i < len) {
                	if(text.charAt(i)=='@'){
                		return i;
                    }else{
                    	i++;
                    }
                }
                return len;
			}
		});
        
        Button tweet = (Button)findViewById(R.id.tweetButton);
        
        tweet.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View v) {
				TweetCakeActivity.twitaccess.setStatus(text.getText().toString());
				//list.dismiss();
			}
		});
	}
	
	@Override
    public void onConfigurationChanged(Configuration c){
    	super.onConfigurationChanged(c);
    }
}
