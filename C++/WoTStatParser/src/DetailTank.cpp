#include "DetailTank.h"

DetailTank::DetailTank(TankPlayed* t){
	//init de l'interface
	l = new QGridLayout();
	setLayout(l);

	generalRandom = new QLabel();
	generalRandom->setText("General Random");
	maxKills = new QLabel();
	maxXP = new QLabel();
	totalXP = new QLabel();
	battleCount = new QLabel();
	wins = new QLabel();
	losses = new QLabel();
	survivedBattles = new QLabel();
	winAndSurvived = new QLabel();
	frags = new QLabel();
	frags8p = new QLabel();
	fragsBeast = new QLabel();
	shots = new QLabel();
	hits = new QLabel();
	spotted = new QLabel();
	damageDealt = new QLabel();
	damageReceived = new QLabel();
	treeCut = new QLabel();
	capturePoints = new QLabel();
	decapPoints = new QLabel();

	l->addWidget(generalRandom, 0, 0, 1, 3, Qt::AlignHCenter);
	l->addWidget(maxKills, 1, 0);
	l->addWidget(maxXP, 1, 1);
	l->addWidget(totalXP, 1, 2);
	l->addWidget(battleCount, 2, 0);
	l->addWidget(wins, 2, 1);
	l->addWidget(losses, 2, 2);
	l->addWidget(survivedBattles, 3, 0);
	l->addWidget(winAndSurvived, 3, 1);
	l->addWidget(frags, 3, 2);
	l->addWidget(frags8p, 4, 0);
	l->addWidget(fragsBeast, 4, 1);
	l->addWidget(shots, 4, 2);
	l->addWidget(hits, 5, 0);
	l->addWidget(spotted, 5, 1);
	l->addWidget(damageDealt, 5, 2);
	l->addWidget(damageReceived, 6, 0);
	l->addWidget(treeCut, 6, 1);
	l->addWidget(capturePoints, 6, 2);
	l->addWidget(decapPoints, 7, 0);

	setInfos(t);
}

void DetailTank::updateTank(TankPlayed* t){
	setInfos(t);
}

void DetailTank::setInfos(TankPlayed* t){
	RandomData *random = &t->m_datas.randomData;
	maxKills->setText(QString("Max Kills : ")+QString::number(random->maxKills));
	maxXP->setText(QString("Max XP : ")+QString::number(random->maxXP));
	totalXP->setText(QString("Total XP : ")+QString::number(random->totalXP));
	battleCount->setText(QString("Nb Battles : ")+QString::number(random->battleCount));
	wins->setText(QString("Wins : ")+QString::number(random->wins)+QString("(")+QString::number((float)random->wins/(float)random->battleCount*100.0f)+QString("%)"));
	losses->setText(QString("Losses : ")+QString::number(random->losses)+QString("(")+QString::number((float)random->losses/(float)random->battleCount*100.0f)+QString("%)"));
	survivedBattles->setText(QString("Survived : ")+QString::number(random->survivedBattles)+QString("(")+QString::number((float)random->survivedBattles/(float)random->battleCount*100.0f)+QString("%)"));
	winAndSurvived->setText(QString("WinsSurvived : ")+QString::number(random->winAndSurvived)+QString("(")+QString::number((float)random->winAndSurvived/(float)random->battleCount*100.0f)+QString("%)"));
	frags->setText(QString("Frags : ")+QString::number(random->frags));
	frags8p->setText(QString("Frags 8+ : ")+QString::number(random->frags8p));
	fragsBeast->setText(QString("Frags Beast : ")+QString::number(random->fragsBeast));
	shots->setText(QString("Shots : ")+QString::number(random->shots));
	hits->setText(QString("Hits : ")+QString::number(random->hits)+QString("(")+QString::number((float)random->hits/(float)random->shots*100.0f)+QString("%)"));
	spotted->setText(QString("Spotted : ")+QString::number(random->spotted));
	damageDealt->setText(QString("Dmg Dealt : ")+QString::number(random->damageDealt));
	damageReceived->setText(QString("Dmg Received : ")+QString::number(random->damageReceived));
	treeCut->setText(QString("? : ")+QString::number(random->treeCut));
	capturePoints->setText(QString("Capture Points : ")+QString::number(random->capturePoints));
	decapPoints->setText(QString("Decap Points : ")+QString::number(random->decapPoints));
}
