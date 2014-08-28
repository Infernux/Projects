#include <QtWidgets/QApplication>

#include "content.h"
#include "Player.h"

//#include <SFML/Graphics.hpp>
//#include "myWindow.h"

//SFML provoque des fuites

using namespace std;

int main(int argc, char** argv)
{
	Player p("./datas/moi.dat");

	QApplication app(argc, argv);

	Content c(&p);

	c.show();
	
	return app.exec();
	//return 0;
}
