package com.LiveZoneStudio.TweetCake;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;

import twitter4j.User;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Bitmap.Config;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.PorterDuff.Mode;
import android.graphics.PorterDuffXfermode;
import android.graphics.Rect;
import android.graphics.RectF;
import android.os.Environment;

public class CacheManager {
	long MONTH =(long) 2592000000.;
	Context mctxt;
	ArrayList<File> aSup = new ArrayList<File>();
	//TODO getProfileImage(java.lang.String screenName, ProfileImage.ImageSize size)
	public CacheManager(Context ctxt){
		mctxt=ctxt;
		File chemin = new File(Environment.getExternalStorageDirectory().getPath()+"/Android/data/TweetCake/");
		isTooBig(chemin);
	}
	
	public Bitmap getBitmap(User u){
		Bitmap b;
		File chemin = new File(Environment.getExternalStorageDirectory().getPath()+"/Android/data/TweetCake/");
		chemin.mkdirs();
		b = BitmapFactory.decodeFile(Environment.getExternalStorageDirectory().getPath()+"/Android/data/TweetCake/"+u.getId());
		if(b == null){
			getImage(u.getProfileImageURL(), u.getId());
			b = BitmapFactory.decodeFile(Environment.getExternalStorageDirectory().getPath()+"/Android/data/TweetCake/"+u.getId());
		}
		
		b=setCorner(b);
		
		return b;
	}
	
	private void isTooBig(File chemin){
		if(chemin.list().length>0){
			long time = System.currentTimeMillis();
			for(File f : chemin.listFiles()){
				if((time-f.lastModified())>MONTH){
					aSup.add(f);
				}
			}
		}
	}
	
	public void purgeFile(){
		for(File f : aSup){
			f.delete();
		}
	}
	
	private Bitmap setCorner(Bitmap b){
		Bitmap output = Bitmap.createBitmap(b.getWidth(), b.getHeight(), Config.ARGB_8888);
        Canvas canvas = new Canvas(output);

        final int color = 0xff424242;
        final Paint paint = new Paint();
        final Rect rect = new Rect(0, 0, b.getWidth(), b.getHeight());
        final RectF rectF = new RectF(rect);
        final float roundPx = 10;

        paint.setAntiAlias(true);
        canvas.drawARGB(0, 0, 0, 0);
        paint.setColor(color);
        canvas.drawRoundRect(rectF, roundPx, roundPx, paint);

        paint.setXfermode(new PorterDuffXfermode(Mode.SRC_IN));
        canvas.drawBitmap(b, rect, rect, paint);
        
        return output;
	}
	
	void getImage(URL url, long id){
		byte [] buf = new byte[1024];
			
		try {
			InputStream is = null;
			is = url.openStream();
			System.out.println(is.available());
					
			File test = new File(Environment.getExternalStorageDirectory().getPath()+"/Android/data/TweetCake/"+id);
			test.createNewFile();
						
			FileOutputStream fos = new FileOutputStream(test);
			BufferedOutputStream bos = new BufferedOutputStream(fos, 1024);
			int nbRead;
		    try {
			        while ((nbRead = is.read(buf)) > 0) {
			            bos.write(buf, 0, nbRead);
		        }
		    } finally {
			        bos.flush();
			        bos.close();
			        fos.flush();
			        fos.close();
			    }
		}catch (IOException e) {
		   	   e.printStackTrace();
		}
	}
	
	static Bitmap dlImage(String url){
		try{
			URL aURL = new URL(url);
			
			URLConnection conn = aURL.openConnection();
			
			conn.setUseCaches(true);
	        conn.connect();
	        if(conn.getContentLength()>=250000)
	        {
	        	return null;
	        }
	        
	        BufferedInputStream bis = new BufferedInputStream(conn.getInputStream(), 8000);
	        
	        Bitmap bm = BitmapFactory.decodeStream(bis);
	        
	
	        bis.close();
	
	        return bm;
		}catch(IOException e){
			
		}
		return null;
	}
}