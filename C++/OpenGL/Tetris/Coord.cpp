#include "Coord.h"

Coord::Coord(int x, int y){
    this->x = x;
    this->y = y;
    alive=true;
}

void Coord::setCoord(int x, int y){
    this->x = x;
    this->y = y;
    alive=true;
}

void Coord::setX(int x){
    this->x=x;
}

void Coord::setY(int y){
    this->y=y;
}

int Coord::getX(){
    return x;
}

int Coord::getY(){
    return y;
}
