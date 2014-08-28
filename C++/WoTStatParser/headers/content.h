#ifndef __CONTENT_H
#define __CONTENT_H

#include <QtWidgets/QWidget>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QTabBar>

#include "Player.h"
#include "detailTab.h"
#include "GeneralInfos.h"

class Content : public QWidget
{
	Q_OBJECT

	public:
		Content(Player *p);

	private:
		QVBoxLayout *l;
		QTabBar *tab;
		DetailTab *dt;
		GeneralInfos *gt;
	
	public slots:
		void changeActiveWidget(int i);
};

#endif
