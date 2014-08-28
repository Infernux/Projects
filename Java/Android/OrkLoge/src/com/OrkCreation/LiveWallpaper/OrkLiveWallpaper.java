package com.OrkCreation.LiveWallpaper;


import java.util.TimeZone;

import android.content.SharedPreferences;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Matrix;
import android.graphics.Paint;
import android.graphics.Rect;
import android.graphics.Typeface;
import android.net.Uri;
import android.os.Handler;
import android.os.SystemClock;
import android.provider.MediaStore;
import android.service.wallpaper.WallpaperService;
import android.util.Log;
import android.view.Display;
import android.view.MotionEvent;
import android.view.SurfaceHolder;
import android.widget.Button;
import android.widget.Toast;

public class OrkLiveWallpaper extends WallpaperService{
	public static final String SHARED_PREFS_NAME="Orkloge_settings";
	
	private final Handler mHandler = new Handler();
	private int mHauteur;
	private int mLargeur;
	private Typeface typeface;
	private Bitmap fond=null;
	
	private boolean editMode=true;
	
	//Préférences
	private SharedPreferences mPrefs=null;

    @Override
    public void onCreate() {
        super.onCreate();
        
        /*mLargeur = this.getApplicationContext().getWallpaperDesiredMinimumWidth()/2;
        mHauteur = this.getApplicationContext().getWallpaperDesiredMinimumHeight();*/
        mLargeur = 480;
        mHauteur = 854;
        typeface = Typeface.createFromAsset(this.getAssets(), "CENTAUR.TTF");
        
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
    }

    @Override
    public Engine onCreateEngine() {
        return new CubeEngine();
    }

    class CubeEngine extends Engine implements SharedPreferences.OnSharedPreferenceChangeListener{
    	
        private final Paint mPaint = new Paint();
        private float mOffset;
        private float mTouchX = -1;
        private float mTouchY = -1;
        private float mCenterX;
        private float mCenterY;
        private int epaisseur, mHauteurMatrice, decalageBarre, decalageTexte, contour=1;
        
        
        //Valeurs Couleurs
        private final int alpha = 0xFF000000;
        private int red = 0x00000000;
        private int green = 0x00000000;
        private int blue = 0x00000000;
        private boolean modifR, modifG, modifB;
        
        private int heures = -1;
        private int minutes;
        
        private String texte;
        
        private boolean couleur=false;
        
        private final Runnable mGetFond = new Runnable(){
        	public void run(){
        		String a = mPrefs.getString("fond", "b");
        		mHandler.removeCallbacks(mGetFond);
    			if(!a.contains("b")){
    				Uri b = Uri.parse(a);
    				String[] filePathColumn = {MediaStore.Images.Media.DATA};
    	
    	            Cursor cursor = getContentResolver().query(b, filePathColumn, null, null, null);
    	            if(cursor!=null){
    		            cursor.moveToFirst();
    		
    		            int columnIndex = cursor.getColumnIndex(filePathColumn[0]);
    		            String filePath = cursor.getString(columnIndex);
    		            cursor.close();
    					
    					fond = BitmapFactory.decodeFile(filePath);
    	            }else{
    	            	mHandler.postDelayed(mGetFond, 2000);
    	            }
    			}
        	}
        };

        private final Runnable mDrawCube = new Runnable() {
            public void run() {
                drawFrame();
            }
        };
        
        private boolean mVisible;

        CubeEngine() {
        	//Recuperation du paint + config
            final Paint paint = mPaint;
            if(!couleur){
            	red = 0x00FF0000;
            	green = 0x0000FF00;
            	blue = 0x000000FF;
            	codeCouleur = alpha+red+green+blue;
            }
            paint.setColor(alpha+green+blue+red);
            paint.setAntiAlias(true);
            paint.setStrokeWidth(2);
            paint.setStrokeCap(Paint.Cap.ROUND);
            paint.setStyle(Paint.Style.FILL);

            //SystemClock.elapsedRealtime();
        }

        @Override
        public void onCreate(SurfaceHolder surfaceHolder) {
            super.onCreate(surfaceHolder);
            mPaint.setTypeface(typeface);
        	decalageBarre = mHauteur/48;
        	decalageTexte = decalageBarre*3;
        	if(mHauteur==854){
        		mHauteurMatrice = mHauteur/10;
        		epaisseur = 14;
        		mPaint.setTextSize(35);
        	}else{
        		mHauteurMatrice = mHauteur/9;
        		epaisseur = 8;
        		mPaint.setTextSize(20);
        	}
        	if(!editMode){
        		setTouchEventsEnabled(false);
        	}else{
        		setTouchEventsEnabled(true);
        	}
        }

        @Override
        public void onDestroy() {
            super.onDestroy();
            mHandler.removeCallbacks(mDrawCube);
            mHandler.removeCallbacks(mGetFond);
        }

        @Override
        public void onVisibilityChanged(boolean visible) {
            mVisible = visible;
            if (visible) {
                drawFrame();
            } else {
                mHandler.removeCallbacks(mDrawCube);
            }
        }

        @Override
        public void onSurfaceChanged(SurfaceHolder holder, int format, int width, int height) {
            super.onSurfaceChanged(holder, format, width, height);
            mCenterX = width/2.0f;
            /*Float tmpF = mPrefs.getFloat("alignement", mHauteur/2.0f);
            mCenterY = tmpF;*/
            mCenterY = height/2.0f;
           	//Log.i("largeur", String.valueOf(tmpF));
            String tmpS = mPrefs.getString("fond", "b");
			if(!tmpS.contains("b")){
				mHandler.postDelayed(mGetFond, 2000);
			}
            drawFrame();
        }

        @Override
        public void onSurfaceCreated(SurfaceHolder holder) {
            super.onSurfaceCreated(holder);

            //Recuperation config
        	mPrefs = OrkLiveWallpaper.this.getSharedPreferences(SHARED_PREFS_NAME, 0);
	        mPrefs.registerOnSharedPreferenceChangeListener(this);
	        onSharedPreferenceChanged(mPrefs, null);
        }

        @Override
        public void onSurfaceDestroyed(SurfaceHolder holder) {
            super.onSurfaceDestroyed(holder);
            mVisible = false;
            mHandler.removeCallbacks(mDrawCube);
            mHandler.removeCallbacks(mGetFond);
        }

        @Override
        public void onOffsetsChanged(float xOffset, float yOffset,
                float xStep, float yStep, int xPixels, int yPixels) {
            mOffset = xOffset;
            drawFrame();
        }

        /*
         * Store the position of the touch event so we can use it for drawing later
         */
        @Override
        public void onTouchEvent(MotionEvent event) {
            if (event.getAction() == MotionEvent.ACTION_MOVE) {
                mTouchX = event.getX();
                mTouchY = event.getY();
                if(editMode){
                	if(mTouchY<(mHauteur-mHauteur/10)){
                		mCenterY = mTouchY;
                	}
                }
            } else {
                mTouchX = -1;
                mTouchY = -1;
            }
            super.onTouchEvent(event);
        }

        /*
         * Draw one frame of the animation. This method gets called repeatedly
         * by posting a delayed Runnable. You can do any drawing you want in
         * here. This example draws a wireframe cube.
         */
        
        void drawFrame() {
            final SurfaceHolder holder = getSurfaceHolder();

            Canvas c = null;
            try {
                c = holder.lockCanvas();
                if (c != null) {
                    drawHeure(c);
                }
            } finally {
                if (c != null) holder.unlockCanvasAndPost(c);
            }

            // Reschedule the next redraw
            mHandler.removeCallbacks(mDrawCube);
            if (mVisible){
                mHandler.postDelayed(mDrawCube, 1000/2);
            }
        }

        /*
         * 
         */
        private int largeurMatrice = mLargeur/6;
        private float gauche1 = largeurMatrice*5/2;
        private float gauche2 = largeurMatrice*3/2;
        private float gauche3 = largeurMatrice/2;
        private int decalageH = largeurMatrice/3;
        private int codeCouleur = alpha+green+blue+red;
        
        //Nombre de caractères faisant partie des minutes
        private int charmin=0;
        
        void drawHeure(Canvas c) {
            c.save();
            c.translate(mCenterX, mCenterY);
            c.drawColor(0xFF000000);
            if(fond!=null){
            	Matrix matrix = new Matrix();
				matrix.setRotate(180.0f, mCenterX ,mCenterY);
            	c.drawBitmap(fond, matrix, mPaint);
            	//c.drawBitmap(fond, -mCenterX, -mCenterY, mPaint);
            	//Log.i("matrice",c.getMatrix().toString());
            }
            //c.drawBitmap(fond, new Rect(0, 0, fond.getWidth(), fond.getHeight()), new RectF(-mCenterX, -mCenterY, mLargeur-mCenterX, mHauteur-mCenterY), mPaint);
            
            //Dessin du fond
            
            texte="";
            long time = System.currentTimeMillis()%86400000;
            TimeZone timeZone = TimeZone.getDefault();
            
            time += timeZone.getOffset(time);
            time += timeZone.getDSTSavings();
            
            if(heures!=time/3600000){
            	heures=(int)time/3600000;
            	if(couleur){
            		mPaint.setColor(getCouleurHeure(heures));
            	}
            }
            setTexte(heures, 0);
            time = time%3600000;
            minutes = (int)time/60000;
            setTexte(minutes, 1);
            if(couleur){
            	mPaint.setColor(getCouleurMinutes(minutes));
            }
            
            drawMatrice(c, heures/10, -gauche1);
            drawMatrice(c, heures%10, -gauche2);
            
            //drawPoints(c, -32);
            drawH(c, -decalageH);
            drawMatrice(c, minutes/10, gauche3);
            drawMatrice(c, minutes%10, gauche2);
            time = time%60000;
            
            drawTexte(c);
            drawBarre(c, -3*largeurMatrice+20, time/600);
            
            c.restore();
        }
        
        void drawTexte(Canvas c){
        	Rect r=new Rect();
            mPaint.getTextBounds(texte, 0, texte.length(), r);
            c.drawText(texte, 0, texte.length()-charmin, -mLargeur/2+(mLargeur-r.right)/2, mHauteurMatrice/2+decalageTexte, mPaint);
            
            int couleurTemp = alpha+green+blue+red;
            int tmpRect = r.right;
            mPaint.setColor(couleurTemp-0x66000000);
            mPaint.getTextBounds(texte, 0, texte.length()-charmin, r);
            
            c.drawText(texte, texte.length()-charmin, texte.length(), -mLargeur/2+(mLargeur-tmpRect)/2+r.right, mHauteurMatrice/2+decalageTexte, mPaint);
            
            mPaint.setColor(couleurTemp);
        }
        
        void setTexte(int valeur, int choix){
        	// 0 : Heures -- 1 : Minutes
        	int tmp = valeur/10;
    		int tmp2 = valeur%10;
        	if(choix==0){
        		
        		if(valeur%24==0){
        			texte+=getResources().getString(R.string.minuit);
        		}else{
	        		switch(tmp){
	        			case 0:
	        				texte+=getTexteNombre(tmp2);
	        				break;
	        			case 1:
	        				switch(tmp2){
		        				case 1:
		        					texte+=getResources().getString(R.string.onze);
		        					break;
		        					
		        				case 2:
		        					texte+=getResources().getString(R.string.douze);
		        					break;
		        					
		        				case 3:
		        					texte+=getResources().getString(R.string.treize);
		        					break;
		        					
		        				case 4:
		        					texte+=getResources().getString(R.string.quatorze);
		        					break;
		        				
		        				case 5:
		        					texte+=getResources().getString(R.string.quinze);
		        					break;
		        					
		        				case 6:
		        					texte+=getResources().getString(R.string.seize);
		        					break;
		        					
		        				case 7:
		        					texte+=getResources().getString(R.string.dixsept);
		        					break;
		        					
		        				case 8:
		        					texte+=getResources().getString(R.string.dixhuit);
		        					break;
		        					
		        				case 9:
		        					texte+=getResources().getString(R.string.dixneuf);
		        					break;
		        					
		        				default:
		        					texte+=getResources().getString(R.string.dix);
		        					texte=texte.toLowerCase();
		        					break;
	        				}
	        				break;
	        			case 2:
	        				texte+=getResources().getString(R.string.vingt);
	        				texte=texte.toLowerCase();
	        				texte+=getTexteNombre(tmp2);
	        				break;
	        		}
        		}
        	}else{
        		if(tmp==1){
        			String tmpString="";
	        		switch(tmp2){
	        		case 1:
    					texte+=getResources().getString(R.string.onze);
    					break;
    					
    				case 2:
    					texte+=getResources().getString(R.string.douze);
    					break;
    					
    				case 3:
    					texte+=getResources().getString(R.string.treize);
    					break;
    					
    				case 4:
    					texte+=getResources().getString(R.string.quatorze);
    					break;
    				
    				case 5:
    					texte+=getResources().getString(R.string.quinze);
    					break;
    					
    				case 6:
    					texte+=getResources().getString(R.string.seize);
    					break;
    					
    				case 7:
    					texte+=getResources().getString(R.string.dixsept);
    					break;
    					
    				case 8:
    					texte+=getResources().getString(R.string.dixhuit);
    					break;
    					
    				case 9:
    					texte+=getResources().getString(R.string.dixneuf);
    					break;
							
					default:
						tmpString+=getResources().getString(R.string.dix);
						break;
	        		}
	        		charmin=tmpString.length();
	        		texte+=tmpString;
        		}else{
        			String tmpString="";
        			tmpString+=getTexteNombreDizaine(tmp);
        			tmpString+=getTexteNombre(tmp2);
        			charmin=tmpString.length();
					texte+=tmpString;
        		}
        	}
        }
        
        String getTexteNombreDizaine(int valeur){
        	String texteRetour="";
        	switch(valeur){
				case 1:
					texteRetour=getResources().getString(R.string.dix);
					break;
					
				case 2:
					texteRetour=getResources().getString(R.string.vingt);
					break;
					
				case 3:
					texteRetour=getResources().getString(R.string.trente);
					break;
					
				case 4:
					texteRetour=getResources().getString(R.string.quarante);
					break;
				
				case 5:
					texteRetour=getResources().getString(R.string.cinquante);
					break;
        	}
        	return texteRetour;
        }
        
        String getTexteNombre(int valeur){
        	String texteRetour="";
        	switch(valeur){
				case 1:
					texteRetour=getResources().getString(R.string.un);
					break;
					
				case 2:
					texteRetour=getResources().getString(R.string.deux);
					break;
					
				case 3:
					texteRetour=getResources().getString(R.string.trois);
					break;
					
				case 4:
					texteRetour=getResources().getString(R.string.quatre);
					break;
				
				case 5:
					texteRetour=getResources().getString(R.string.cinq);
					break;
					
				case 6:
					texteRetour=getResources().getString(R.string.six);
					break;
					
				case 7:
					texteRetour=getResources().getString(R.string.sept);
					break;
					
				case 8:
					texteRetour=getResources().getString(R.string.huit);
					break;
					
				case 9:
					texteRetour=getResources().getString(R.string.neuf);
					break;
        	}
        	return texteRetour;
        }
        
        int offset = 10;
        
        void drawMatrice(Canvas c, int chiffre, float gauche){
        	int noir = 0x22000000;
        	//DebutX, DebutY, FinX, FinY
        	switch(chiffre){
        		case 0:
        			drawTop(c, gauche, offset);
                	drawLeft(c, gauche, offset);
                	drawRight(c, gauche, offset);
                	drawBot(c, gauche, offset);
                	mPaint.setColor(noir);
                	drawContourHoriTExt(c, offset, gauche+offset, gauche+largeurMatrice);
                	drawContourHoriTInt(c, offset, gauche+offset+epaisseur, gauche+largeurMatrice-epaisseur);
                	drawContourHoriBInt(c, offset, gauche+offset+epaisseur, gauche+largeurMatrice-epaisseur);
                	drawContourHoriBExt(c, offset, gauche+offset, gauche+largeurMatrice);
                	
                	drawContourVerticalGExt(c, gauche, offset, -mHauteurMatrice/2, mHauteurMatrice/2);
                	drawContourVerticalGInt(c, gauche, offset, -mHauteurMatrice/2+epaisseur, mHauteurMatrice/2-epaisseur);
                	drawContourVerticalDExt(c, gauche, offset, -mHauteurMatrice/2, mHauteurMatrice/2);
                	drawContourVerticalDInt(c, gauche, offset, -mHauteurMatrice/2+epaisseur, mHauteurMatrice/2-epaisseur);
                	break;
                	
        		case 1:
                	drawRight(c, gauche, offset);
                	mPaint.setColor(noir);
                	drawContourHoriTExt(c, offset, gauche+largeurMatrice-epaisseur, gauche+largeurMatrice);
                	drawContourHoriBExt(c, offset, gauche+largeurMatrice-epaisseur, gauche+largeurMatrice);
                	drawContourVerticalDExt(c, gauche, offset, -mHauteurMatrice/2, mHauteurMatrice/2);
                	drawContourVerticalDInt(c, gauche, offset, -mHauteurMatrice/2, mHauteurMatrice/2);
                	break;
                	
        		case 2:
        			drawTop(c, gauche, offset);
                	drawTopRight(c, gauche, offset);
                	drawCenter(c, gauche, offset);
                	drawBotLeft(c, gauche, offset);
                	drawBot(c, gauche, offset);
                	
                	mPaint.setColor(noir);
                	drawContourHoriTExt(c, offset, gauche+offset, gauche+largeurMatrice);
                	drawContourHoriTInt(c, offset, gauche+offset, gauche+largeurMatrice-epaisseur);
                	drawContourHoriCExt(c, offset, gauche+offset, gauche+largeurMatrice-epaisseur);
                	drawContourHoriCInt(c, offset, gauche+offset+epaisseur, gauche+largeurMatrice);
                	drawContourHoriBInt(c, offset, gauche+offset+epaisseur, gauche+largeurMatrice);
                	drawContourHoriBExt(c, offset, gauche+offset, gauche+largeurMatrice);
                	
                	drawContourVerticalGExt(c, gauche, offset, -mHauteurMatrice/2, -mHauteurMatrice/2+epaisseur);
                	drawContourVerticalGExt(c, gauche, offset, -epaisseur/2, mHauteurMatrice/2);
                	drawContourVerticalGInt(c, gauche, offset, epaisseur/2, mHauteurMatrice/2-epaisseur);
                	drawContourVerticalDInt(c, gauche, offset, -mHauteurMatrice/2+epaisseur, -epaisseur/2);
                	drawContourVerticalDExt(c, gauche, offset, -mHauteurMatrice/2, epaisseur/2);
                	drawContourVerticalDExt(c, gauche, offset, mHauteurMatrice/2-epaisseur, mHauteurMatrice/2);
                	
                	break;
                	
        		case 3:
        			drawTop(c, gauche, offset);
                	drawRight(c, gauche, offset);
                	drawCenter(c, gauche, offset);
                	drawBot(c, gauche, offset);
                	
                	mPaint.setColor(noir);
                	drawContourHoriTExt(c, offset, gauche+offset, gauche+largeurMatrice);
                	drawContourHoriTInt(c, offset, gauche+offset, gauche+largeurMatrice-epaisseur);
                	drawContourHoriCExt(c, offset, gauche+offset, gauche+largeurMatrice-epaisseur);
                	drawContourHoriCInt(c, offset, gauche+offset, gauche+largeurMatrice-epaisseur);
                	drawContourHoriBInt(c, offset, gauche+offset, gauche+largeurMatrice-epaisseur);
                	drawContourHoriBExt(c, offset, gauche+offset, gauche+largeurMatrice);
                	drawContourVerticalGExt(c, gauche, offset, -mHauteurMatrice/2, -mHauteurMatrice/2+epaisseur);
                	drawContourVerticalGExt(c, gauche, offset, -epaisseur/2, epaisseur/2);
                	drawContourVerticalGExt(c, gauche, offset, mHauteurMatrice/2-epaisseur, mHauteurMatrice/2);
                	drawContourVerticalDInt(c, gauche, offset, -mHauteurMatrice/2+epaisseur, -epaisseur/2);
                	drawContourVerticalDInt(c, gauche, offset, epaisseur/2, mHauteurMatrice/2-epaisseur);
                	drawContourVerticalDExt(c, gauche, offset, -mHauteurMatrice/2, mHauteurMatrice/2);
                	
                	break;
                	
        		case 4:
        			drawTopLeft(c, gauche, offset);
        			drawCenter(c, gauche, offset);
        			drawRight(c, gauche, offset);
        			
        			mPaint.setColor(noir);
        			drawContourHoriTExt(c, offset, gauche+offset, gauche+offset+epaisseur);
        			drawContourHoriTExt(c, offset, gauche+largeurMatrice-epaisseur, gauche+largeurMatrice);
        			drawContourHoriCExt(c, offset, gauche+offset+epaisseur, gauche+largeurMatrice-epaisseur);
        			drawContourHoriCInt(c, offset, gauche+offset, gauche+largeurMatrice-epaisseur);
        			drawContourHoriBExt(c, offset, gauche+largeurMatrice-epaisseur, gauche+largeurMatrice);
        			drawContourVerticalGExt(c, gauche, offset, -mHauteurMatrice/2, epaisseur/2);
        			drawContourVerticalGInt(c, gauche, offset, -mHauteurMatrice/2, -epaisseur/2);
        			drawContourVerticalDInt(c, gauche, offset, -mHauteurMatrice/2, -epaisseur/2);
        			drawContourVerticalDInt(c, gauche, offset, epaisseur/2, mHauteurMatrice/2);
        			drawContourVerticalDExt(c, gauche, offset, -mHauteurMatrice/2, mHauteurMatrice/2);
        			break;
        			
        		case 5:
        			drawTop(c, gauche, offset);
        			drawTopLeft(c, gauche, offset);
        			drawCenter(c, gauche, offset);
        			drawBotRight(c, gauche, offset);
        			drawBot(c, gauche, offset);
        			
        			mPaint.setColor(noir);
        			drawContourHoriTExt(c, offset, gauche+offset, gauche+largeurMatrice);
        			drawContourHoriTInt(c, offset, gauche+offset+epaisseur, gauche+largeurMatrice);
        			drawContourHoriCExt(c, offset, gauche+offset+epaisseur, gauche+largeurMatrice);
        			drawContourHoriCInt(c, offset, gauche+offset, gauche+largeurMatrice-epaisseur);
        			drawContourHoriBInt(c, offset, gauche+offset, gauche+largeurMatrice-epaisseur);
        			drawContourHoriBExt(c, offset, gauche+offset, gauche+largeurMatrice);
        			
        			drawContourVerticalGExt(c, gauche, offset, -mHauteurMatrice/2, epaisseur/2);
        			drawContourVerticalGExt(c, gauche, offset, mHauteurMatrice/2-epaisseur, mHauteurMatrice/2);
        			drawContourVerticalGInt(c, gauche, offset, -mHauteurMatrice/2+epaisseur, -epaisseur/2);
        			drawContourVerticalDInt(c, gauche, offset, epaisseur/2, mHauteurMatrice/2-epaisseur);
        			drawContourVerticalDExt(c, gauche, offset, -mHauteurMatrice/2, -mHauteurMatrice/2+epaisseur);
        			drawContourVerticalDExt(c, gauche, offset, -epaisseur/2, mHauteurMatrice/2);
        			break;
        			
        		case 6:
        			drawTop(c, gauche, offset);
        			drawLeft(c, gauche, offset);
        			drawBot(c, gauche, offset);
        			drawBotRight(c, gauche, offset);
        			drawCenter(c, gauche, offset);
        			
        			mPaint.setColor(noir);
        			drawContourHoriTExt(c, offset, gauche+offset, gauche+largeurMatrice);
        			drawContourHoriTInt(c, offset, gauche+offset+epaisseur, gauche+largeurMatrice);
        			drawContourHoriCExt(c, offset, gauche+offset+epaisseur, gauche+largeurMatrice);
        			drawContourHoriCInt(c, offset, gauche+offset+epaisseur, gauche+largeurMatrice-epaisseur);
        			drawContourHoriBInt(c, offset, gauche+offset+epaisseur, gauche+largeurMatrice-epaisseur);
        			drawContourHoriBExt(c, offset, gauche+offset, gauche+largeurMatrice);
        			
        			drawContourVerticalGExt(c, gauche, offset, -mHauteurMatrice/2, mHauteurMatrice/2);
        			drawContourVerticalGInt(c, gauche, offset, -mHauteurMatrice/2+epaisseur, -epaisseur/2);
        			drawContourVerticalGInt(c, gauche, offset, epaisseur/2, mHauteurMatrice/2-epaisseur);
        			drawContourVerticalDInt(c, gauche, offset, epaisseur/2, mHauteurMatrice/2-epaisseur);
        			drawContourVerticalDExt(c, gauche, offset, -mHauteurMatrice/2, -mHauteurMatrice/2+epaisseur);
        			drawContourVerticalDExt(c, gauche, offset, -epaisseur/2, mHauteurMatrice/2);
        			break;
        			
        		case 7:
        			drawTop(c, gauche, offset);
        			drawRight(c, gauche, offset);
        			
        			mPaint.setColor(noir);
        			drawContourHoriTExt(c, offset, gauche+offset, gauche+largeurMatrice);
        			drawContourHoriTInt(c, offset, gauche+offset, gauche+largeurMatrice-epaisseur);
        			drawContourHoriBExt(c, offset, gauche+largeurMatrice-epaisseur, gauche+largeurMatrice);
        			
        			drawContourVerticalGExt(c, gauche, offset, -mHauteurMatrice/2, -mHauteurMatrice/2+epaisseur);
        			drawContourVerticalDInt(c, gauche, offset, -mHauteurMatrice/2+epaisseur, mHauteurMatrice/2);
        			drawContourVerticalDExt(c, gauche, offset, -mHauteurMatrice/2, mHauteurMatrice/2);
        			break;
        			
        		case 8:
        			drawTop(c, gauche, offset);
        			drawLeft(c, gauche, offset);
        			drawRight(c, gauche, offset);
        			drawBot(c, gauche, offset);
        			drawCenter(c, gauche, offset);
        			
        			mPaint.setColor(noir);
        			drawContourHoriTExt(c, offset, gauche+offset, gauche+largeurMatrice);
                	drawContourHoriTInt(c, offset, gauche+offset+epaisseur, gauche+largeurMatrice-epaisseur);
                	drawContourHoriCExt(c, offset, gauche+offset+epaisseur, gauche+largeurMatrice-epaisseur);
                	drawContourHoriCInt(c, offset, gauche+offset+epaisseur, gauche+largeurMatrice-epaisseur);
                	drawContourHoriBInt(c, offset, gauche+offset+epaisseur, gauche+largeurMatrice-epaisseur);
                	drawContourHoriBExt(c, offset, gauche+offset, gauche+largeurMatrice);
                	
        			drawContourVerticalGExt(c, gauche, offset, -mHauteurMatrice/2, mHauteurMatrice/2);
        			drawContourVerticalGInt(c, gauche, offset, -mHauteurMatrice/2+epaisseur, -epaisseur/2);
        			drawContourVerticalGInt(c, gauche, offset, epaisseur/2, mHauteurMatrice/2-epaisseur);
        			drawContourVerticalDInt(c, gauche, offset, -mHauteurMatrice/2+epaisseur, -epaisseur/2);
        			drawContourVerticalDInt(c, gauche, offset, epaisseur/2, mHauteurMatrice/2-epaisseur);
        			drawContourVerticalDExt(c, gauche, offset, -mHauteurMatrice/2, mHauteurMatrice/2);
        			break;
        			
        		case 9:
        			drawTop(c, gauche, offset);
        			drawTopLeft(c, gauche, offset);
        			drawCenter(c, gauche, offset);
        			drawRight(c, gauche, offset);
        			drawBot(c, gauche, offset);
        			
        			mPaint.setColor(noir);
        			drawContourHoriTExt(c, offset, gauche+offset, gauche+largeurMatrice);
                	drawContourHoriTInt(c, offset, gauche+offset+epaisseur, gauche+largeurMatrice-epaisseur);
                	drawContourHoriCExt(c, offset, gauche+offset+epaisseur, gauche+largeurMatrice-epaisseur);
                	drawContourHoriCInt(c, offset, gauche+offset, gauche+largeurMatrice-epaisseur);
                	drawContourHoriBInt(c, offset, gauche+offset, gauche+largeurMatrice-epaisseur);
                	drawContourHoriBExt(c, offset, gauche+offset, gauche+largeurMatrice);
        			
        			drawContourVerticalGExt(c, gauche, offset, -mHauteurMatrice/2, epaisseur/2);
        			drawContourVerticalGExt(c, gauche, offset, mHauteurMatrice/2-epaisseur, mHauteurMatrice/2);
        			drawContourVerticalGInt(c, gauche, offset, -mHauteurMatrice/2+epaisseur, -epaisseur/2);
        			drawContourVerticalDInt(c, gauche, offset, -mHauteurMatrice/2+epaisseur, -epaisseur/2);
        			drawContourVerticalDInt(c, gauche, offset, epaisseur/2, mHauteurMatrice/2-epaisseur);
        			drawContourVerticalDExt(c, gauche, offset, -mHauteurMatrice/2, mHauteurMatrice/2);
        			break;
        			
        		default:
        			break;
        	}
        	mPaint.setColor(codeCouleur);
        }
        
        void drawBarre(Canvas c, float gauche, float progress){
        	float a = progress/100*(6*largeurMatrice-40);
        	//c.drawLine(gauche, mHauteurMatrice/2+10, gauche+a, mHauteurMatrice/2+10, mPaint);
        	if(!couleur){
        		mPaint.setColor(0xFF999999);
        	}
        	c.drawRect(gauche, mHauteurMatrice/2+decalageBarre, gauche+a, mHauteurMatrice/2+decalageBarre+2, mPaint);
        	mPaint.setColor(0xFFFFFFFF);
        	//c.drawLine(gauche+a, mHauteurMatrice/2+10, -gauche, mHauteurMatrice/2+10, mPaint);
        	c.drawRect(gauche+a, mHauteurMatrice/2+decalageBarre, -gauche, mHauteurMatrice/2+decalageBarre+2, mPaint);
        }
        
        /*void drawPoints(Canvas c, int gauche){
        	c.drawCircle(0, -25, 5, mPaint);
        	c.drawCircle(0, 25, 5, mPaint);
        }*/
        
        void drawH(Canvas c, float gauche){
        	drawLeft(c, gauche, 3);
        	drawCenter(c, gauche, 3, decalageH);
        	drawRight(c, gauche, 3, decalageH);
        	
        	mPaint.setColor(0x22000000);
        	drawContourHoriTExt(c, offset, gauche+3, gauche+epaisseur+3);
        	drawContourHoriTExt(c, offset, gauche+decalageH*2-epaisseur+3, gauche+decalageH*2+3);
        	drawContourHoriCExt(c, offset, gauche+epaisseur+3, gauche+decalageH*2-epaisseur);
        	drawContourHoriCInt(c, offset, gauche+epaisseur+3, gauche+decalageH*2-epaisseur);
        	drawContourHoriBExt(c, offset, gauche+3, gauche+epaisseur+3);
        	drawContourHoriBExt(c, offset, gauche+decalageH*2-epaisseur+3, gauche+decalageH*2+3);
        	
			drawContourVerticalGExt(c, gauche, 3, -mHauteurMatrice/2, mHauteurMatrice/2);
			drawContourVerticalGInt(c, gauche, 3, -mHauteurMatrice/2, -epaisseur/2);
			drawContourVerticalGInt(c, gauche, 3, epaisseur/2, mHauteurMatrice/2);
			drawContourVerticalDInt(c, gauche, offset, -mHauteurMatrice/2, -epaisseur/2, decalageH);
			drawContourVerticalDInt(c, gauche, offset, epaisseur/2, mHauteurMatrice/2, decalageH);
			drawContourVerticalDExt(c, gauche, offset, -mHauteurMatrice/2, mHauteurMatrice/2, decalageH);
		
			mPaint.setColor(codeCouleur);
        }
        
        void drawTop(Canvas c, float gauche, int offset){
        	c.drawRect(gauche+offset, -mHauteurMatrice/2, gauche+largeurMatrice, -mHauteurMatrice/2+epaisseur, mPaint);
        }
        
        void drawLeft(Canvas c, float gauche, int offset){
        	c.drawRect(gauche+offset, -mHauteurMatrice/2, gauche+offset+epaisseur, mHauteurMatrice/2, mPaint);
        }
        
        void drawRight(Canvas c, float gauche, int offset){
        	//c.drawLine(gauche+64-offset, -mHauteurMatrice/2, gauche+64-offset, mHauteurMatrice/2, mPaint);
        	c.drawRect(gauche+largeurMatrice-epaisseur, -mHauteurMatrice/2, gauche+largeurMatrice, mHauteurMatrice/2, mPaint);
        }
        
        void drawRight(Canvas c, float gauche, int offset, int droite){
        	//c.drawLine(gauche+64-offset, -mHauteurMatrice/2, gauche+64-offset, mHauteurMatrice/2, mPaint);
        	c.drawRect(gauche+decalageH*2+offset-epaisseur, -mHauteurMatrice/2, gauche+decalageH*2+offset, mHauteurMatrice/2, mPaint);
        }
        
        void drawTopLeft(Canvas c, float gauche, int offset){
        	//c.drawLine(gauche+offset, -mHauteurMatrice/2, gauche+offset, 0, mPaint);
        	c.drawRect(gauche+offset, -mHauteurMatrice/2, gauche+offset+epaisseur, 0, mPaint);
        }
        
        void drawBotLeft(Canvas c, float gauche, int offset){
        	//c.drawLine(gauche+offset, 0, gauche+offset, mHauteurMatrice/2, mPaint);
        	c.drawRect(gauche+offset, 0, gauche+offset+epaisseur, mHauteurMatrice/2, mPaint);
        }
        
        void drawTopRight(Canvas c, float gauche, int offset){
        	c.drawRect(gauche+largeurMatrice-epaisseur, -mHauteurMatrice/2, gauche+largeurMatrice, 0, mPaint);
        }
        
        void drawBotRight(Canvas c, float gauche, int offset){
        	//c.drawLine(gauche+64-offset, 0, gauche+64-offset, mHauteurMatrice/2, mPaint);
        	c.drawRect(gauche+largeurMatrice-epaisseur, 0, gauche+largeurMatrice, mHauteurMatrice/2, mPaint);
        }
        
        void drawBot(Canvas c, float gauche, int offset){
        	//c.drawLine(gauche+offset, mHauteurMatrice/2, gauche+64-offset, mHauteurMatrice/2, mPaint);
        	c.drawRect(gauche+offset, mHauteurMatrice/2-epaisseur, gauche+largeurMatrice, mHauteurMatrice/2, mPaint);
        }
        
        void drawCenter(Canvas c, float gauche, int offset){
        	//c.drawLine(gauche+offset, 0, gauche+64-offset, 0, mPaint);
        	c.drawRect(gauche+offset, -epaisseur/2, gauche+largeurMatrice, epaisseur/2, mPaint);
        }
        
        void drawCenter(Canvas c, float gauche, int offset, int droite){
        	//c.drawLine(gauche+offset, 0, gauche+64-offset, 0, mPaint);
        
        	c.drawRect(gauche+offset, -epaisseur/2, droite, epaisseur/2, mPaint);
        }
        
        /**
         * M�thode pour les contours
         * Vertical puis Horizontal
         * 
         * 10 m�thodes
         * 
         * G = Gauche
         * D = Droite
         * 
         * Ext = Exterieur
         * Int = Interieur
         */
        
        void drawContourVerticalGExt(Canvas c, float gauche, int offset, int debut, int fin){
        	c.drawRect(gauche+offset-contour, debut, gauche+offset, fin, mPaint);
        }
        
        void drawContourVerticalGInt(Canvas c, float gauche, int offset, int debut, int fin){
        	c.drawRect(gauche+offset+epaisseur, debut, gauche+offset+epaisseur+contour, fin, mPaint);
        }
        
        void drawContourVerticalDExt(Canvas c, float gauche, int offset, int debut, int fin){
        	c.drawRect(gauche+largeurMatrice, debut, gauche+largeurMatrice+contour, fin, mPaint);
        }
        
        void drawContourVerticalDExt(Canvas c, float gauche, int offset, int debut, int fin, int decalage){
        	c.drawRect(gauche+largeurMatrice-decalage, debut, gauche+largeurMatrice+contour-decalage, fin, mPaint);
        }
        
        void drawContourVerticalDInt(Canvas c, float gauche, int offset, int debut, int fin){
        	c.drawRect(gauche+largeurMatrice-epaisseur-contour, debut, gauche+largeurMatrice-epaisseur, fin, mPaint);
        }
        
        void drawContourVerticalDInt(Canvas c, float gauche, int offset, int debut, int fin, int decalage){
        	c.drawRect(gauche+largeurMatrice-epaisseur-contour-decalage, debut, gauche+largeurMatrice-epaisseur-decalage, fin, mPaint);
        }
        
        void drawContourHoriTExt(Canvas c, int offset, float debut, float fin){
        	c.drawRect(debut, -mHauteurMatrice/2-contour, fin, -mHauteurMatrice/2, mPaint);
        }
        
        void drawContourHoriTInt(Canvas c, int offset, float debut, float fin){
        	c.drawRect(debut, -mHauteurMatrice/2+epaisseur, fin, -mHauteurMatrice/2+epaisseur+contour, mPaint);
        }
        
        void drawContourHoriCExt(Canvas c, int offset, float debut, float fin){
        	c.drawRect(debut, -epaisseur/2-contour, fin, -epaisseur/2, mPaint);
        }
        
        void drawContourHoriCInt(Canvas c, int offset, float debut, float fin){
        	c.drawRect(debut, epaisseur/2, fin, epaisseur/2+contour, mPaint);
        }
        
        void drawContourHoriBInt(Canvas c, int offset, float debut, float fin){
        	c.drawRect(debut, mHauteurMatrice/2-epaisseur-contour, fin, mHauteurMatrice/2-epaisseur, mPaint);
        }
        
        void drawContourHoriBExt(Canvas c, int offset, float debut, float fin){
        	c.drawRect(debut, mHauteurMatrice/2, fin, mHauteurMatrice/2+contour, mPaint);
        }
        
        /**
         * 
         * Fin des contours
         * 
         */
        
        int getCouleurHeure(int heure){
        	if(heure<4){
        		red=0x00FF0000;
        		green=0x00005500*heure;
        		modifR=false;
        		modifG=false;
        		modifB=true;
        		return(alpha+red+green);
        	}else if(heure<8){
        		green=0x0000FF00;
        		red=0x00FF0000-(heure%4)*0x00550000;
        		modifR=false;
        		modifG=false;
        		modifB=true;
        		return(alpha+green+red);
        	}else if(heure<12){
        		green=0x0000FF00;
        		blue=0x00000055*(heure%4);
        		modifR=true;
        		modifG=false;
        		modifB=false;
        		return(alpha+green+blue);
        	}else if(heure<16){
        		blue=0x000000FF;
        		green=0x0000FF00-(heure%4)*0x00005500;
        		modifR=true;
        		modifG=false;
        		modifB=false;
        		return(alpha+blue+green);
        	}else if(heure<20){
        		blue=0x000000FF;
        		red=(heure%4)*0x00550000;
        		modifR=false;
        		modifG=true;
        		modifB=false;
        		return(alpha+blue+red);
        	}else{
        		red=0x00FF0000;
        		blue=0x000000FF-(heure%4)*0x00000055;
        		modifR=false;
        		modifG=true;
        		modifB=false;
        		return(alpha+red+blue);
        	}
        }
        
        int getCouleurMinutes(int minutes){
        	if(modifR){
        		red=0x00000000+minutes*0x00040000;
        	}
        	if(modifG){
        		green=0x00000000+minutes*0x00000400;
        	}
        	if(modifB){
        		blue=0x00000000+minutes*0x00000004;
        	}
        	codeCouleur = alpha+red+green+blue;
        	return(alpha+red+green+blue);
        }
        /*
         * Draw a circle around the current touch point, if any.
         */
        void drawTouchPoint(Canvas c) {
            if (mTouchX >=0 && mTouchY >= 0) {
                c.drawCircle(mTouchX, mTouchY, 80, mPaint);
            }
        }
        
        void resetColor(){
        	red = 0x00000000;
			green = 0x00000000;
			blue = 0x00000000;
			heures=-1;
        }

		@Override
		public void onSharedPreferenceChanged(
				SharedPreferences sharedPreferences, String key) {
			if(sharedPreferences!=null){
				String a = sharedPreferences.getString("couleur", "true");
				
				if(a.contains("true")){
					couleur = true;
					resetColor();
				}else{
					couleur = false;
					red = 0x00FF0000;
					green = 0x0000FF00;
					blue = 0x000000FF;
					codeCouleur = alpha+red+green+blue;
				}
				editMode = sharedPreferences.getBoolean("editMode", false);
				
				if(key!=null){
					if(!key.contains("alignement")){
						SharedPreferences.Editor edit = sharedPreferences.edit();
						edit.putFloat("alignement", mCenterY);
				    	edit.commit();
					}
				}
				
				
				mHandler.postDelayed(mGetFond, 2000);
				drawFrame();
			}
		}

    }
}