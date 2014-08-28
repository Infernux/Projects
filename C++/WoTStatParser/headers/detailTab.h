#ifndef __DETAILTAB_H
#define __DETAILTAB_H

#include <QtWidgets/QWidget>
#include <QtWidgets/QLabel>
#include <QtWidgets/QBoxLayout>
#include <QtWidgets/QListWidget>
#include <QtWidgets/QScrollArea>

#include "Player.h"
#include "TankPlayed.h"
#include "DetailTank.h"

class DetailTab : public QWidget
{
	Q_OBJECT

	public:
		DetailTab(Player *p);
	private:
		Player *player;
		QBoxLayout *layout;
		QListWidget *list;
		QScrollArea *scroll;
		DetailTank *detail;
	public slots:
		void slotUpdateTank(int i);
};

#endif
