#include "Piece.h"

Piece::Piece(Coord grid, Vector3D abs, Coord mesh[], Coord center, Color fill, Color stroke){
    gridCoord=grid;
    absCoord=abs;
    this->mesh=mesh;
    this->center=center;
    fillColor=fill;
    strokeColor=stroke;
}

Piece::~Piece(){
    delete mesh;
}

Coord* Piece::getGridCoords(){
    return &gridCoord;
}

Vector3D* Piece::getAbsCoords(){
    return &absCoord;
}

Coord* Piece::getMesh(int pos){
    if(pos<0 || pos>=meshSize)
        return NULL;

    return &mesh[pos];
}

Coord* Piece::getCenter(){
    return &center;
}

Color* Piece::getFillColor(){
    return &fillColor;
}

Color* Piece::getStrokeColor(){
    return &strokeColor;
}

void Piece::setGridCoords(Coord c){
    gridCoord.setCoord(c.getX(), c.getY());
}

void Piece::setAbsCoords(Vector3D c){
    absCoord.x = c.x;
    absCoord.y = c.y;
    absCoord.z = c.z;
}

void Piece::setMesh(Coord mesh[], int size){
    this->mesh=mesh;
    meshSize=size;
}

void Piece::setCenter(Coord c){
    center.setCoord(c.getX(), c.getY());
}

void Piece::setFillColor(Color c){
    fillColor.setValues(c.getRed(), c.getGreen(), c.getBlue());
}

void Piece::setStrokeColor(Color c){
    strokeColor.setValues(c.getRed(), c.getGreen(), c.getBlue());
}
