#include "Line.h"

Line::Line() : Piece(Coord(0,0), Vector3D(0,0,0), NULL, Coord(0,0), Color(0,255,1), Color(2,2,2)){
    meshSize=4;
    mesh = (Coord*)malloc(sizeof(Coord)*meshSize);
    mesh[0].setCoord(-1,0);
    mesh[1].setCoord(0,0);
    mesh[2].setCoord(1,0);
    mesh[3].setCoord(2,0);
}

Line::~Line(){
    //freeing the mesh is done in Piece class
}
