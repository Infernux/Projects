package com.LiveZoneStudio.skydiver;

import org.anddev.andengine.engine.Engine;
import org.anddev.andengine.engine.camera.BoundCamera;
import org.anddev.andengine.engine.camera.hud.HUD;
import org.anddev.andengine.engine.camera.hud.controls.AnalogOnScreenControl;
import org.anddev.andengine.engine.camera.hud.controls.BaseOnScreenControl;
import org.anddev.andengine.engine.camera.hud.controls.AnalogOnScreenControl.IAnalogOnScreenControlListener;
import org.anddev.andengine.engine.handler.IUpdateHandler;
import org.anddev.andengine.engine.options.EngineOptions;
import org.anddev.andengine.engine.options.EngineOptions.ScreenOrientation;
import org.anddev.andengine.engine.options.resolutionpolicy.RatioResolutionPolicy;
import org.anddev.andengine.entity.layer.tiled.tmx.TMXLayer;
import org.anddev.andengine.entity.layer.tiled.tmx.TMXLoader;
import org.anddev.andengine.entity.layer.tiled.tmx.TMXProperties;
import org.anddev.andengine.entity.layer.tiled.tmx.TMXTile;
import org.anddev.andengine.entity.layer.tiled.tmx.TMXTileProperty;
import org.anddev.andengine.entity.layer.tiled.tmx.TMXTiledMap;
import org.anddev.andengine.entity.layer.tiled.tmx.TMXLoader.ITMXTilePropertiesListener;
import org.anddev.andengine.entity.layer.tiled.tmx.util.exception.TMXLoadException;
import org.anddev.andengine.entity.primitive.Rectangle;
import org.anddev.andengine.entity.scene.Scene;
import org.anddev.andengine.entity.scene.background.ColorBackground;
import org.anddev.andengine.entity.scene.background.IBackground;
import org.anddev.andengine.entity.scene.popup.PopupScene;
import org.anddev.andengine.entity.scene.popup.TextPopupScene;
import org.anddev.andengine.entity.shape.Shape;
import org.anddev.andengine.entity.sprite.AnimatedSprite;
import org.anddev.andengine.entity.sprite.Sprite;
import org.anddev.andengine.entity.text.Text;
import org.anddev.andengine.entity.util.FPSLogger;
import org.anddev.andengine.extension.input.touch.controller.MultiTouchController;
import org.anddev.andengine.extension.input.touch.controller.MultiTouchException;
import org.anddev.andengine.extension.physics.box2d.PhysicsConnector;
import org.anddev.andengine.extension.physics.box2d.PhysicsFactory;
import org.anddev.andengine.extension.physics.box2d.PhysicsWorld;
import org.anddev.andengine.extension.physics.box2d.util.Vector2Pool;
import org.anddev.andengine.input.touch.TouchEvent;
import org.anddev.andengine.opengl.IDrawable;
import org.anddev.andengine.opengl.font.Font;
import org.anddev.andengine.opengl.font.FontLibrary;
import org.anddev.andengine.opengl.texture.Texture;
import org.anddev.andengine.opengl.texture.TextureOptions;
import org.anddev.andengine.opengl.texture.region.TextureRegion;
import org.anddev.andengine.opengl.texture.region.TextureRegionFactory;
import org.anddev.andengine.opengl.texture.region.TiledTextureRegion;
import org.anddev.andengine.ui.activity.BaseGameActivity;
import org.anddev.andengine.util.Debug;
import org.anddev.andengine.util.HorizontalAlign;

import com.badlogic.gdx.math.Vector2;
import com.badlogic.gdx.physics.box2d.Body;
import com.badlogic.gdx.physics.box2d.FixtureDef;
import com.badlogic.gdx.physics.box2d.MassData;
import com.badlogic.gdx.physics.box2d.BodyDef.BodyType;

import android.app.Activity;
import android.content.Context;
import android.graphics.Color;
import android.graphics.Typeface;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.util.Log;
import android.view.Display;
import android.view.MotionEvent;
import android.view.WindowManager;

public class SkyDiver extends BaseGameActivity {
	private static final float DEMO_VELOCITY = 250.0f;
    private static final float DEMO_GRAVITY = 9.81f;
    
    /*Display display = ((WindowManager) getSystemService(Context.WINDOW_SERVICE)).getDefaultDisplay();
    final int cameraWidth = display.getWidth();
    final int cameraHeight = display.getHeight();*/
    
    private static final FixtureDef FIXTURE_DEF = PhysicsFactory.createFixtureDef(0, 0f, 0f);
    
    private static int CAMERA_WIDTH;
    private static int CAMERA_HEIGHT;
    private static float largeurLvl;
    private static float hauteurLvl;
    
    boolean monte = true;
    
    private long[] animLast = new long[]{100, 100, 100, 100};
    
    //int[][] collisionList=null;
    
    private TMXTiledMap mTMXTiledMap;
    private PhysicsWorld mPhysicsWorld;
    
    private Font f;
    private Text mText;
    private String hint;
    private Shape panneau;
    
    private BoundCamera mCamera;
    private Texture mTexture;
	private TiledTextureRegion mBallTextureRegion;
	private TiledTextureRegion mPersoDTextureRegion;
	private TextureRegion mBackground;
	private TextureRegion mPadTextureRegion;
	private TextureRegion mFlecheTextureRegion;
	private TextureRegion mKnobTextureRegion;

	@Override
	public Engine onLoadEngine() {
		Display display = ((WindowManager) getSystemService(Context.WINDOW_SERVICE)).getDefaultDisplay();
		CAMERA_WIDTH = display.getWidth();
	    CAMERA_HEIGHT = display.getHeight();
		this.mCamera = new BoundCamera(0, 0, CAMERA_WIDTH, CAMERA_HEIGHT);
	    
        return new Engine(new EngineOptions(true, ScreenOrientation.LANDSCAPE,
                new RatioResolutionPolicy(CAMERA_WIDTH, CAMERA_HEIGHT),
                this.mCamera));
	}

	@Override
	public void onLoadResources() {
		this.mTexture = new Texture(2048, 2048,
                TextureOptions.BILINEAR_PREMULTIPLYALPHA);
        this.mBallTextureRegion = TextureRegionFactory.createTiledFromAsset(
                this.mTexture, this, "gfx/ball.png", 0, 0, 1, 1);
        this.mPadTextureRegion = TextureRegionFactory.createFromAsset(this.mTexture, this, "gfx/Viseur.png", 148, 0);
        this.mPersoDTextureRegion = TextureRegionFactory.createTiledFromAsset(this.mTexture, this, "gfx/test.png", 179, 0 , 8, 1);
        this.mKnobTextureRegion = TextureRegionFactory.createFromAsset(this.mTexture, this, "gfx/boule.png", 424, 0);
        this.mFlecheTextureRegion = TextureRegionFactory.createFromAsset(this.mTexture, this, "gfx/fleche.png", 475, 0);
        this.mBackground = TextureRegionFactory.createFromAsset(this.mTexture, this, "gfx/fond.png", 540, 0);
        //this.mPersoGTextureRegion = TextureRegionFactory.createTiledFromAsset(this.mTexture, this, "gfx/mario_tiled_G.png", 179, 0 , 4, 1);

        this.mEngine.getTextureManager().loadTexture(this.mTexture);
	}
	//int largeurTile;
	@Override
	public Scene onLoadScene() {
        
		try {
			this.mEngine.setTouchController(new MultiTouchController());
		} catch (MultiTouchException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
        this.mPhysicsWorld = new PhysicsWorld(new Vector2(0, SensorManager.GRAVITY_EARTH), false);
		
		Typeface tf = Typeface.createFromAsset(this.getAssets(), "CENTAUR.TTF");
    	
    	Texture texture = new Texture(256, 256, TextureOptions.BILINEAR_PREMULTIPLYALPHA);
    	f = new Font(texture, tf, 15, true, Color.BLACK);
    	this.mEngine.getTextureManager().loadTexture(texture);
    	this.mEngine.getFontManager().loadFont(f);
		
		HUD mHud = new HUD();
		
		final FixtureDef wallFixtureDef = PhysicsFactory.createFixtureDef(0f, 0f, 0f);
		
		this.mEngine.registerUpdateHandler(new FPSLogger());
		
        final Scene scene = new Scene(3);
        //scene.setBackground(new ColorBackground(0.09804f, 0.6274f, 0.8784f));
        
        try {
            final TMXLoader tmxLoader = new TMXLoader(this, this.mEngine.getTextureManager(), TextureOptions.BILINEAR_PREMULTIPLYALPHA, new ITMXTilePropertiesListener() {
                    @Override
                    public void onTMXTileWithPropertiesCreated(final TMXTiledMap pTMXTiledMap, final TMXLayer pTMXLayer, final TMXTile pTMXTile, final TMXProperties<TMXTileProperty> pTMXTileProperties){
                    	/*if(collisionList==null){
                            //initalize variable
                            collisionList = new int[pTMXLayer.getTileRows()][pTMXLayer.getTileColumns()];
                    	}*/
	                    if (pTMXTileProperties.containsTMXProperty("Collidable", "true")) {
	                    	float X = pTMXTile.getTileColumn()*32.0f;
	                    	float Y = pTMXTile.getTileRow()*32.0f;
	                    	
	                    	final Shape square = new Rectangle(X, Y, 32.0f, 32.0f);
	                    	//Log.i("Pos", String.valueOf(X));
	                    	PhysicsFactory.createBoxBody(SkyDiver.this.mPhysicsWorld, square, BodyType.StaticBody, wallFixtureDef);
	                    	//scene.getTopLayer().addEntity(square);
	                        //collisionList[pTMXTile.getTileRow()][pTMXTile.getTileColumn()] = 1;
	                    }else{
		                    if(pTMXTileProperties.containsTMXProperty("isInfo", "true")){
		                    	float X = pTMXTile.getTileColumn()*32.0f;
		                    	float Y = pTMXTile.getTileRow()*32.0f;
		                    	
		                    	panneau = new Rectangle(X, Y, 32.0f, 32.0f){
		                    		public boolean onAreaTouched(final TouchEvent pSceneTouchEvent, final float pTouchAreaLocalX, final float pTouchAreaLocalY){
		                                if (pSceneTouchEvent.getAction() == MotionEvent.ACTION_DOWN){
		                                    Log.i("Touch", "Oui");
		                                }
		                 
		                                return true;
		                            }
		                        };
		                    	hint = new String();
		                        //collisionList[pTMXTile.getTileRow()][pTMXTile.getTileColumn()] = 2;
		                        hint = pTMXTileProperties.get(0).getValue().toString();
		                    }
	                    }
                    }
            });
            this.mTMXTiledMap = tmxLoader.loadFromAsset(this, "tmx/nuage.tmx");

	    } catch (final TMXLoadException tmxle) {
	            Debug.e(tmxle);
	    }
	    final TMXLayer tmxLayer = this.mTMXTiledMap.getTMXLayers().get(0);
		largeurLvl = tmxLayer.getWidth();
        hauteurLvl = tmxLayer.getHeight();
        
	    scene.getLayer(1).addEntity(tmxLayer);
	    
	    //final Shape ground = new Rectangle(0, hauteurLvl - 2, largeurLvl, 2);
        final Shape roof = new Rectangle(0, 0, largeurLvl, 2);
        final Shape left = new Rectangle(0, 0, 2, hauteurLvl);
        final Shape right = new Rectangle(largeurLvl - 2, 0, 2, hauteurLvl);
        
        //PhysicsFactory.createBoxBody(this.mPhysicsWorld, ground, BodyType.StaticBody, wallFixtureDef);
        PhysicsFactory.createBoxBody(this.mPhysicsWorld, roof, BodyType.StaticBody, wallFixtureDef);
        PhysicsFactory.createBoxBody(this.mPhysicsWorld, left, BodyType.StaticBody, wallFixtureDef);
        PhysicsFactory.createBoxBody(this.mPhysicsWorld, right, BodyType.StaticBody, wallFixtureDef);
	    
        final Perso mario = new Perso(50, 0, this.mPersoDTextureRegion);
        mCamera.setChaseShape(mario);
        final Body body = PhysicsFactory.createBoxBody(this.mPhysicsWorld, mario, BodyType.DynamicBody, FIXTURE_DEF);
        
        MassData mMassData = new MassData();
        mMassData.mass=70;
        body.setMassData(mMassData);
        this.mPhysicsWorld.registerPhysicsConnector(new PhysicsConnector(mario, body, true, false, true, false));
        this.mCamera.setBounds(0, tmxLayer.getWidth(), 0, tmxLayer.getHeight());
        this.mCamera.setBoundsEnabled(true);
        
        
        mario.setStuck(1, largeurLvl);
        mario.setStuck(0, hauteurLvl);
        
        final AnalogOnScreenControl pad = new AnalogOnScreenControl(5, CAMERA_HEIGHT -
                this.mFlecheTextureRegion.getHeight()-5, this.mCamera, this.mFlecheTextureRegion,
                this.mKnobTextureRegion, 0.1f, 200,  new IAnalogOnScreenControlListener(){
        	// Gauche == -1; Nul == 0; Droite == 1
        	int sens=0;
        	@Override
            public void onControlChange(final BaseOnScreenControl pBaseOnScreenControl, final float
                            pValueX, final float pValueY){
                    if (pValueX != 0){
                            //float rotationInRad = (float)Math.atan2(-pValueX, pValueY);
                            mario.setMouvement(true);
                            /*mario.setStuck(-1, 0);
                            mario.setStuck(1, largeurLvl);
                            if(!mario.getJumpState()){
                            	mario.setStuck(2, 0);
                            }
                            mario.setStuck(0, hauteurLvl);*/
                            if(pValueX>0&&(mario.getX()<mario.getStuck(1))){
                            	if(sens!=1){
                            		mario.stopAnimation();
                            	}
                            	sens=1;
                            	final Vector2 velocity = Vector2Pool.obtain();
                            	velocity.set(pValueX*5, body.getLinearVelocity().y);
    							body.setLinearVelocity(velocity);
    							Vector2Pool.recycle(velocity);
    							
    							if(!mario.isAnimationRunning()){
	    							mario.animate(animLast, 4, 7, true);
    							}
    						}else if(pValueX<0&&(mario.getX()>mario.getStuck(-1)+0.1f)){
    							if(sens!=-1){
                            		mario.stopAnimation();
                            	}
    							sens=-1;
    							//mario.setAccelerationX(-100);
    							final Vector2 velocity = Vector2Pool.obtain();
                            	velocity.set(pValueX*5, body.getLinearVelocity().y);
    							body.setLinearVelocity(velocity);
    							Vector2Pool.recycle(velocity);
    							
    							if(!mario.isAnimationRunning()){
    								mario.animate(animLast, 0, 3, true);
    							}
    						}
                            //mBot.body.setTransform(mBot.body.getWorldCenter(), rotationInRad);                     
                    }else{
                    	mario.setMouvement(false);
                    	//mario.setStuck(0, hauteurLvl);
                    	if(sens==1){
                    		mario.stopAnimation(4);
                    	}else{
                    		mario.stopAnimation(3);
                    	}
                            //stopRot = true;
                    }
            }
			@Override
			public void onControlClick(
					AnalogOnScreenControl pAnalogOnScreenControl) {
				
			}
    	});
        
        pad.setTouchAreaBindingEnabled(true);
        
        final Sprite padJump = new Sprite(CAMERA_WIDTH-mPadTextureRegion.getWidth()-10, CAMERA_HEIGHT-mPadTextureRegion.getHeight()-10,
                this.mPadTextureRegion) {
            @Override
            public boolean onAreaTouched(final TouchEvent pSceneTouchEvent,
                    final float pTouchAreaLocalX, final float pTouchAreaLocalY) {
            	if(!mario.getJumpState()){
                   	//mario.setStuck(2, 0);
	            	mario.setJumpState(true);
	            	mario.setContact(false);
	            	final Vector2 velocity = Vector2Pool.obtain();
                	velocity.set(body.getLinearVelocity().x, -7);
					body.setLinearVelocity(velocity);
					Vector2Pool.recycle(velocity);
            	}
                return true;
            }
        };
        padJump.setScale(2);
 
        final Ball ball = new Ball(CAMERA_HEIGHT, 50, this.mBallTextureRegion);
        ball.setVelocity(DEMO_VELOCITY, DEMO_VELOCITY);
 
        mHud.setChildScene(pad);
        pad.getTopLayer().addEntity(padJump);
        pad.registerTouchArea(padJump);
        mCamera.setHUD(mHud);
        
        Sprite background = new Sprite(0, 0, this.largeurLvl, this.hauteurLvl, mBackground);
        scene.getBottomLayer().addEntity(background);
        
        //scene.getBottomLayer().addEntity(pad);
        scene.getTopLayer().addEntity(ball);
        scene.getTopLayer().addEntity(mario);
        //scene.getTopLayer().addEntity(pad);

        //scene.getTopLayer().addEntity(ground);
        scene.getTopLayer().addEntity(roof);
        scene.getTopLayer().addEntity(left);
        scene.getTopLayer().addEntity(right);

        scene.registerUpdateHandler(this.mPhysicsWorld);
 
        scene.setTouchAreaBindingEnabled(true);
 
        scene.registerUpdateHandler(new IUpdateHandler() {
 
            @Override
            public void reset() {
            }
 
            @Override
            public void onUpdate(final float pSecondsElapsed) {
            	//Ralentissement Horizontal
            	if(mario.inMouvement==false){
            		if(body.getLinearVelocity().x>2){
            			body.setLinearVelocity(new Vector2(body.getLinearVelocity().x-0.2f, body.getLinearVelocity().y));
            		}else if(body.getLinearVelocity().x<-2){
            			body.setLinearVelocity(new Vector2(body.getLinearVelocity().x+0.2f, body.getLinearVelocity().y));
            		}else{
            			body.setLinearVelocity(new Vector2(0, body.getLinearVelocity().y));
            		}
            	}
            	
            	if(body.getLinearVelocity().y==0 && !monte){
            		mario.setJumpState(false);
            	}
            	
            	if(body.getLinearVelocity().y>0.5f){
            		if(mario.getY()>=mCamera.getMaxY()){
            			SkyDiver.this.finish();
            		}
            		mario.setJumpState(true);
            	}
            	
            	if(body.getLinearVelocity().y<=0 && mario.getJumpState()){
            		monte = true;
            	}else{
            		monte = false;
            	}
            	
            	if(mario.collidesWith(panneau)){
            		displayHint(scene);
            		scene.registerTouchArea(panneau);
            		//panneau.onAreaTouched(new TouchEvent(), 0, 0);
            	}else{
            		if(hintDisplayed){
            			scene.getTopLayer().removeEntity(mText);
            		}
            		scene.unregisterTouchArea(panneau);
            		hintDisplayed=false;
            	}
 
                /*SkyDiver.this.runOnUpdateThread(new Runnable() {
 
                    @Override
                    public void run() {
                    	
                    }
                });*/
            }
        });
 
        return scene;
	}
	
	@Override
	public void onLoadComplete() {
		// TODO Auto-generated method stub
		
	}
	
    private static class Ball extends AnimatedSprite {
    	boolean inMouvement=true;
        public Ball(final float pX, final float pY,
                final TiledTextureRegion pTextureRegion) {
            super(pX, pY, pTextureRegion);
        }

        @Override
        protected void onManagedUpdate(final float pSecondsElapsed) {
        	
        	if(this.getVelocityY()<=1000 && this.mY!=0){
        		this.accelerate(0, DEMO_GRAVITY);
        	}
        	
        	if(!inMouvement){
        		if(this.getVelocityX()>5){
        			this.setAccelerationX(-100);
        		}else if(this.getVelocityX()<-5){
        			this.setAccelerationX(100);
        		}else{
        			this.setAccelerationX(0);
        			this.setVelocityX(0);
        		}
        	}else{
        		if(!((this.getVelocityX()>0 && this.getAccelerationX()<0)||(this.getVelocityX()<0 && this.getAccelerationX()>0))){
        			if(this.getVelocityX()>200 || this.getVelocityX()<-200){
                		this.setAccelerationX(0);
                	}
        		}
        	}
        	
            if (this.mX < 0) {
                this.setVelocityX(DEMO_VELOCITY/2);
            } else if (this.mX + this.getWidth() > largeurLvl) {
                this.setVelocityX(-DEMO_VELOCITY/2);
            }
            if (this.mY < 0) {
                this.setVelocityY(-this.getVelocityY());
            } else if (this.mY + this.getHeight() > hauteurLvl){
            	this.mY=CAMERA_HEIGHT-this.getHeight();
            	//this.setVelocityY(-this.getVelocityY()/2);
            	this.setAccelerationY(-this.getAccelerationY()/2);
            }
            
            this.setVelocityY(this.getAccelerationY()*pSecondsElapsed);
            this.setVelocityX(this.getAccelerationX()*pSecondsElapsed+this.getVelocityX());

            super.onManagedUpdate(pSecondsElapsed);
        }
    }
    
    private static class Perso extends AnimatedSprite {
    	private boolean inMouvement=true;
    	private boolean inJump=false;
    	private boolean contact=false;
    	private float stuckG=0, stuckD=800, stuckB, stuckT=0;
    	
        public Perso(final float pX, final float pY,
                final TiledTextureRegion pTextureRegion) {
            super(pX, pY, pTextureRegion);
        }
        
        //-1 == Gauche && 1 == Droite
        public void setStuck(int choix, float f){
        	if(choix==-1){
        		stuckG=f;
        	}else if(choix==1){
        		stuckD=f;
        	}else if(choix==0){
        		stuckB=f;
        	}else{
        		stuckT=f;
        	}
        }
        
        public float getStuck(int choix){
        	if(choix==-1){
        		return stuckG;
        	}else if(choix==1){
        		return stuckD;
        	}else if(choix==0){
        		return stuckB;
        	}else{
        		return stuckT;
        	}
        }
        
        public void setX(float f) {
			this.mX=f;
		}

		public void setY(float f) {
			this.mY=f;
		}

		public void setMouvement(boolean b){
        	inMouvement = b;
        }
        
        public void setJumpState(boolean b){
        	inJump = b;
        }
        
        public void setContact(boolean b){
        	contact = b;
        }
        
        public boolean getContact(){
        	return contact;
        }
        
        public boolean getJumpState(){
        	return inJump;
        }

        @Override
        protected void onManagedUpdate(final float pSecondsElapsed) {
        	/*if(this.getVelocityY()<=300&&!this.getContact()){
        		this.accelerate(0, DEMO_GRAVITY);
        	}else{
        		this.setAccelerationY(0);
        	}*/
        	
        	if(!inMouvement){
        		if(this.getVelocityX()>5){
        			this.setAccelerationX(-200);
        		}else if(this.getVelocityX()<-5){
        			this.setAccelerationX(200);
        		}else{
        			this.setAccelerationX(0);
        			this.setVelocityX(0);
        		}
        	}else{
        		if(!((this.getVelocityX()>0 && this.getAccelerationX()<0)||(this.getVelocityX()<0 && this.getAccelerationX()>0))){
        			if(this.getVelocityX()>200 || this.getVelocityX()<-200){
                		this.setAccelerationX(0);
                	}
        		}
        	}
        	
            if (this.mX < 0) {
                this.setVelocityX(DEMO_VELOCITY/2);
            } else if (this.mX + this.getWidth() > largeurLvl) {
            	this.mY=largeurLvl-this.getWidth();
            	this.setVelocityY(0);
            	this.setAccelerationY(0);
            }
            
            if (this.mY < 0) {
                this.setVelocityY(-this.getVelocityY());
            } /*else if(this.mY+this.getHeight()>hauteurLvl){
            	this.mY=hauteurLvl-this.getHeight();
            	this.setJumpState(false);
            	this.setVelocityY(0);
            	this.setAccelerationY(0);
            }*/
                        
            this.setVelocityY(this.getAccelerationY()*pSecondsElapsed+this.getVelocityY());
            this.setVelocityX(this.getAccelerationX()*pSecondsElapsed+this.getVelocityX());

            super.onManagedUpdate(pSecondsElapsed);
        }
    }
    boolean hintDisplayed=false;
    private void displayHint(Scene scene){
    	if(!hintDisplayed){
	    	mText = new Text(0, mCamera.getCenterY(), f, hint, HorizontalAlign.CENTER);
	    	scene.getTopLayer().addEntity(mText);
	    	hintDisplayed = true;
    	}
    }
}