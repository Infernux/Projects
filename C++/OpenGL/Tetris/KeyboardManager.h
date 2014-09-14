#ifndef __KEYBOARDMANAGER_H
#define __KEYBOARDMANAGER_H

#include <SFML/System.hpp>
#include <SFML/Graphics.hpp>

class KeyboardManager
{
    public :
        bool forward;
        bool backward;
        bool left;
        bool right;
        bool strafeLeft;
        bool strafeRight;
        bool up;
        bool down;

        bool pad1Up;
        bool pad1Down;
        bool pad2Up;
        bool pad2Down;

        KeyboardManager();
        void getInputs(sf::RenderWindow *app);
};

#endif
