#ifndef __DETAILTANK_H
#define __DETAILTANK_H

#include <QtWidgets/QWidget>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QLabel>
#include "TankPlayed.h"
#include "TankKilled.h"
#include "struct.h"

class DetailTank : public QWidget
{
	public:
		DetailTank(TankPlayed* t);
		void updateTank(TankPlayed* t);

	private:
		void setInfos(TankPlayed* t);
		
		QGridLayout *l;
		//Random
		QLabel *generalRandom;
		QLabel *maxKills;
		QLabel *maxXP;
		QLabel *totalXP;
		QLabel *battleCount;
		QLabel *wins;
		QLabel *losses;
		QLabel *survivedBattles;
		QLabel *winAndSurvived;
		QLabel *frags;
		QLabel *frags8p;
		QLabel *fragsBeast;
		QLabel *shots;
		QLabel *hits;
		QLabel *spotted;
		QLabel *damageDealt;
		QLabel *damageReceived;
		QLabel *treeCut;
		QLabel *capturePoints;
		QLabel *decapPoints;
};

#endif
