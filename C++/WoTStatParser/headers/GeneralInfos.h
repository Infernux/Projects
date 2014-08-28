#ifndef __GENERALINFOS_H
#define __GENERALINFOS_H

#include <QtWidgets/QWidget>
#include <QtWidgets/QLabel>
#include <QtWidgets/QGridLayout>

#include "Player.h"

class GeneralInfos : public QWidget
{
	public:
		GeneralInfos(Player *p);	

	private:
		void setInfos(Player *p);

		QGridLayout *l;
		QLabel *total;
		QLabel *wins;
		QLabel *losses;
		QLabel *survived;
};

#endif
