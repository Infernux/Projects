package com.LiveZoneStudio.TweetCake;

public class ElapsedTime {
	private int annees, mois, jours, heures, minutes, secondes;
	
	public ElapsedTime(long time){
		/** Transformation en Secondes */
		time/=1000;
		
		heures=(int)(time/3600);
		time%=3600;
		minutes=(int)(time/60);
		time%=60;
		secondes=(int)(time);
		
		/** Calculés à partir des heures*/
		jours=heures/24;
		heures%=24;
		mois=jours/30;
		jours%=30;
		annees=mois/12;
		mois%=12;
	}
	
	public int getAnnees(){
		return annees;
	}
	
	public int getMois(){
		return mois;
	}
	
	public int getJours(){
		return jours;
	}
	
	public int getHeures(){
		return heures;
	}
	
	public int getMinutes(){
		return minutes;
	}
	
	public int getSecondes(){
		return secondes;
	}
}
