#include "KeyboardManager.h"

KeyboardManager::KeyboardManager(){
    forward = false;
    backward = false;
    strafeLeft = false;
    strafeRight = false;
    up = false;
    down = false;
    left = false;
    right = false;
}

void KeyboardManager::getInputs(sf::RenderWindow *app){
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::Up)){
        up = true;
    }else{
        up = false;
    }
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::Left)){
        left = true;
    }else{
        left = false;
    }
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::Down)){
        down = true;
    }else{
        down = false;
    }
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::Right)){
        right = true;
    }else{
        right = false;
    }
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::S)){
        backward = true;
    }else{
        backward = false;
    }
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::Z)){
        forward = true;
    }else{
        forward = false;
    }
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::Q)){
        strafeLeft = true;
    }else{
        strafeLeft = false;
    }
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::D)){
        strafeRight = true;
    }else{
        strafeRight = false;
    }

    //Pad1
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::T)){
        pad1Up = true;
    }else{
        pad1Up = false;
    }
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::G)){
        pad1Down = true;
    }else{
        pad1Down = false;
    }
    //Pad2
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::I)){
        pad2Up = true;
    }else{
        pad2Up = false;
    }
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::K)){
        pad2Down = true;
    }else{
        pad2Down = false;
    }
}
