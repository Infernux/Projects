#ifndef __MYWINDOW_H
#define __MYWINDOW_H

#include <SFML/Graphics.hpp>

class myWindow
{
	public:
		myWindow();
		myWindow(sf::RenderWindow *win);
		~myWindow();

	private:
		sf::RenderWindow *app;
		int height, width;

};

#endif
