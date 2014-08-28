#include "content.h"

Content::Content(Player *p){
	setMinimumWidth(500);
	dt = new DetailTab(p);

	l = new QVBoxLayout();

	tab = new QTabBar;
	tab->addTab("General");
	tab->addTab("Tank");

	QObject::connect(tab, SIGNAL(currentChanged(int)), this, SLOT(changeActiveWidget(int)));

	gt = new GeneralInfos(p);

	l->addWidget(tab);
	l->addWidget(gt);

	setLayout(l);
}
		
void Content::changeActiveWidget(int i){
	QLayoutItem *item = l->itemAt(1);
	item->widget()->hide();
	l->removeWidget(item->widget());
	
	//b->setText(QString::number(i));
	switch(i){
		case 0:
			l->addWidget(gt);
			gt->show();
			break;

		case 1:
			l->addWidget(dt);
			dt->show();
			break;
	}
	l->invalidate();
}
