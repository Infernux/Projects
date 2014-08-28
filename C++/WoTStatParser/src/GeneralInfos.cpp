#include "GeneralInfos.h"

GeneralInfos::GeneralInfos(Player *p){
	l = new QGridLayout();
	setLayout(l);

	total = new QLabel();
	wins = new QLabel();
	losses = new QLabel();
	survived = new QLabel();

	l->addWidget(total, 0, 0);
	l->addWidget(wins, 0, 1);
	l->addWidget(losses, 0, 2);
	l->addWidget(survived, 1, 0);

	setInfos(p);
}

void GeneralInfos::setInfos(Player *p){
	total->setText(QString("Total : ")+QString::number(p->total));
	Stats *stats = &p->stats;
	wins->setText(QString("Wins : ")+QString::number(stats->wins)+QString("(")+QString::number((float)stats->wins/(float)p->total*100.0f)+QString("%)"));
	losses->setText(QString("Losses : ")+QString::number(stats->losses)+QString("(")+QString::number((float)stats->losses/(float)p->total*100.0f)+QString("%)"));
	survived->setText(QString("Survived : ")+QString::number(stats->survivedBattles)+QString("(")+QString::number((float)stats->survivedBattles/(float)p->total*100.0f)+QString("%)"));
}
