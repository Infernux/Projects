#ifndef __PIECE_H
#define __PIECE_H

#include <SFML/Graphics.hpp>
#include <SFML/OpenGL.hpp>

#include <iostream>

#include "Coord.h"
#include "Vector3D.h"
#include "Color.h"

class Piece {
    public:
       Piece(Coord grid, Vector3D abs, Coord mesh[], Coord center, Color fill, Color stroke);
       ~Piece();

       //getters
       Coord* getGridCoords();
       Vector3D* getAbsCoords();
       Coord* getMesh(int pos);
       Coord* getCenter();
       Color* getFillColor();
       Color* getStrokeColor();

       //setters
       void setGridCoords(Coord c);
       void setAbsCoords(Vector3D c);
       void setMesh(Coord mesh[], int size);
       void setCenter(Coord c);
       void setFillColor(Color c);
       void setStrokeColor(Color c);
        
    protected:
        Coord gridCoord; //logical coords
        Vector3D absCoord; //absolute coord to draw
        Coord *mesh; //collisions
        int meshSize;
        Coord center; //needed ?
        Color fillColor;
        Color strokeColor;
};

#endif
