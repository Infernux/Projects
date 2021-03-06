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
    free(mesh);
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
    absCoord.setX(c.getX());
    absCoord.setY(c.getY());
    absCoord.setZ(c.getZ());
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

void Piece::rotate(){
    for(int i=0; i<meshSize; ++i){
        if(!mesh[i].alive)
            continue;

        int x = mesh[i].getX();
        mesh[i].setX(mesh[i].getY());
        mesh[i].setY(-x);
    }
}

void Piece::draw(GLUquadric *params){
    glColor3ub(fillColor.getRed(), fillColor.getGreen(), fillColor.getBlue());
    glPushMatrix();
    glTranslated(absCoord.getX(), absCoord.getY(), absCoord.getZ());
    for(int i=0; i<meshSize; ++i){
        if(mesh[i].alive)
            drawCube(&mesh[i]);
    }
    glPopMatrix();
}

//protected methods
void Piece::drawCube(Coord *coord){
    drawCube(coord->getX(), coord->getY());
}

void Piece::drawCube(int dx, int dz){
    glPushMatrix();
    glTranslated(dx*SIZE, 0*SIZE, dz*SIZE);
    glBegin(GL_QUADS);
        //left
        //glNormal3f(-1.f, 0.f, 0.f);
        glVertex3d(-1, 1, -1);
        glVertex3d(-1, 1, 1);
        glVertex3d(-1, -1, 1);
        glVertex3d(-1, -1, -1);
    
        //back
        //glNormal3f(0.f, -1.f, 0.f);
        glVertex3d(-1, -1, -1);
        glVertex3d(-1, -1, 1);
        glVertex3d(1, -1, 1);
        glVertex3d(1, -1, -1);
    
        //right
        //glNormal3f(1.f, 0.f, 0.f);
        glVertex3d(1, -1, -1);
        glVertex3d(1, -1, 1);
        glVertex3d(1, 1, 1);
        glVertex3d(1, 1, -1);
    
        //front
        //glNormal3f(0.f, 1.f, 0.f);
        glVertex3d(-1, 1, -1);
        glVertex3d(-1, 1, 1);
        glVertex3d(1, 1, 1);
        glVertex3d(1, 1, -1);

        //top
        //glNormal3f(0.f, 0.f, 1.f);
        glVertex3d(-1, 1, -1);
        glVertex3d(-1, -1, -1);
        glVertex3d(1, -1, -1);
        glVertex3d(1, 1, -1);

        //bottom
        //glNormal3f(0.f, 0.f, -1.f);
        glVertex3d(-1, 1, 1);
        glVertex3d(-1, -1, 1);
        glVertex3d(1, -1, 1);
        glVertex3d(1, 1, 1);
    glEnd();
    glPopMatrix();
}
