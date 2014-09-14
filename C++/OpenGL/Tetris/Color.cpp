#include "Color.h"

Color::Color(int r, int g, int b){
    red=r;
    green=g;
    blue=b;
}

void Color::setValues(int r, int g, int b){
    red=r;
    green=g;
    blue=b;
}

void Color::setRed(int v){
    red=v;
}

void Color::setGreen(int v){
    green=v;
}

void Color::setBlue(int v){
    blue=v;
}

int Color::getRed(){
    return red;
}

int Color::getGreen(){
    return green;
}

int Color::getBlue(){
    return blue;
}
