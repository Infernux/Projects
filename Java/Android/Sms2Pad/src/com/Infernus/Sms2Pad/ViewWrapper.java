package com.Infernus.Sms2Pad;

import android.view.View;
import android.widget.RadioButton;
import android.widget.TextView;

public class ViewWrapper {
	View base;
	TextView nom;
	RadioButton selecteur;
	
	ViewWrapper(View base/*, Bitmap iconeURL, String nomt, Bitmap dispoURL, String prixt, String URLobjet*/){
		this.base=base;
		/*image.setImageBitmap(iconeURL);
		nom.setText(nomt);
		dispo.setImageBitmap(dispoURL);
		prix.setText(prixt);*/
	}
	
	TextView getNom(){
		if(nom==null)
		{
			nom=(TextView)base.findViewById(R.id.nom);
		}
		return nom;
	}
	
	RadioButton getSelecteur(){
		if(selecteur==null)
		{
			selecteur = (RadioButton)base.findViewById(R.id.selecteur);
		}
		return selecteur;
	}
}
