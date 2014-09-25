#include "Square.h"

Square::Square() : Piece(Coord(0,0), Vector3D(0,0,0), NULL, Coord(0,0), Color(255,1,1), Color(2,2,2)){
    meshSize=4;
    mesh = (Coord*)malloc(sizeof(Coord)*meshSize);
    mesh[0].setCoord(-1,-1);
    mesh[1].setCoord(-1,0);
    mesh[2].setCoord(0,0);
    mesh[3].setCoord(0,-1);
}

Square::~Square(){
    //freeing the mesh is done in Piece class
}
