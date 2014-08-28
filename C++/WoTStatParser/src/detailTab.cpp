#include <detailTab.h>

DetailTab::DetailTab(Player *p){
	player = p;
	layout = new QBoxLayout(QBoxLayout::LeftToRight);
	scroll = new QScrollArea();
	scroll->setWidgetResizable(true);
	setLayout(layout);

	list = new QListWidget();
	list->setFixedWidth(200);
	layout->addWidget(list);

	for(int i=0; i<p->tanks.size(); ++i){
		TankPlayed *tank = p->tanks[i];
		QListWidgetItem *item = new QListWidgetItem;
		item->setText(QString::fromStdString(tank->m_name->c_str()));
		list->addItem(item);
	}

	detail = new DetailTank(p->tanks.front());
	scroll->setWidget(detail);
	layout->addWidget(scroll, Qt::AlignLeft);

	QObject::connect(list, SIGNAL(currentRowChanged(int)), this, SLOT(slotUpdateTank(int)));
}

void DetailTab::slotUpdateTank(int i){
	detail->updateTank(player->tanks[i]);
}
