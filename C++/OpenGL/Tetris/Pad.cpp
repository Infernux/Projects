#include "Pad.h"

Pad::Pad(){
    red = 255;
    green = 255;
    blue = 255;
    z = 0;
    x = 0;
    height = 5;
}

Pad::~Pad(){
}

void Pad::setColor(int r, int g, int b){
    red = r;
    green = g;
    blue = b;
}

void Pad::draw(GLUquadric *params){
    glPushMatrix();
    glTranslated(x, 0, z);
    //en regardant de direction y=-1
    glBegin(GL_QUADS);
        //left
        glNormal3f(-1.f, 0.f, 0.f);
        glColor3ub(red, green, blue);
        glVertex3d(-1, 1, -height);
        glVertex3d(-1, 1, height);
        glVertex3d(-1, -1, height);
        glVertex3d(-1, -1, -height);

        //back
        glNormal3f(0.f, -1.f, 0.f);
        glColor3ub(red-20, green, blue);
        glVertex3d(-1, -1, -height);
        glVertex3d(-1, -1, height);
        glVertex3d(1, -1, height);
        glVertex3d(1, -1, -height);

        //right
        glNormal3f(1.f, 0.f, 0.f);
        glColor3ub(red, green-20, blue);
        glVertex3d(1, -1, -height);
        glVertex3d(1, -1, height);
        glVertex3d(1, 1, height);
        glVertex3d(1, 1, -height);

        //front
        glNormal3f(0.f, 1.f, 0.f);
        glColor3ub(red, green, blue-20);
        glVertex3d(-1, 1, -height);
        glVertex3d(-1, 1, height);
        glVertex3d(1, 1, height);
        glVertex3d(1, 1, -height);

        //top
        glNormal3f(0.f, 0.f, 1.f);
        glColor3ub(red, green-20, blue-20);
        glVertex3d(-1, 1, height);
        glVertex3d(-1, -1, height);
        glVertex3d(1, -1, height);
        glVertex3d(1, 1, height);

        //bottom
        glNormal3f(0.f, 0.f, -1.f);
        glColor3ub(red-20, green-20, blue-20);
        glVertex3d(-1, 1, -height);
        glVertex3d(-1, -1, -height);
        glVertex3d(1, -1, -height);
        glVertex3d(1, 1, -height);
    glEnd();
    glPopMatrix();
}

void Pad::setX(int newX){
    x = newX;
}

float Pad::getZ(){
    return z;
}

void Pad::up(float elapsed){
    if(z<7){
        z+=elapsed;
    }else{
        z=7;
    }
}

void Pad::down(float elapsed){
    if(z>-7){
        z-=elapsed;
    }else{
        z=-7;
    }
}

void Pad::loadTextures(){
    img = new sf::Image();
    if(!img->loadFromFile("rocket_top.jpg")){
        return;
    }
    img->flipVertically();
    glGenTextures(1, &texTop);
    glBindTexture(GL_TEXTURE_2D, texTop);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img->getSize().x, img->getSize().y, 0,
            GL_RGBA, GL_UNSIGNED_BYTE, img->getPixelsPtr());
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glBindTexture(GL_TEXTURE_2D, 0); //dévérouillage

    if(!img->loadFromFile("rocket_middle.jpg")){
        return;
    }
    img->flipVertically();
    glGenTextures(1, &texMiddle);
    glBindTexture(GL_TEXTURE_2D, texMiddle);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img->getSize().x, img->getSize().y, 0,
            GL_RGBA, GL_UNSIGNED_BYTE, img->getPixelsPtr());
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glBindTexture(GL_TEXTURE_2D, 0); //dévérouillage

    if(!img->loadFromFile("rocket_bottom.jpg")){
        return;
    }
    img->flipVertically();
    glGenTextures(1, &texBot);
    glBindTexture(GL_TEXTURE_2D, texBot);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img->getSize().x, img->getSize().y, 0,
            GL_RGBA, GL_UNSIGNED_BYTE, img->getPixelsPtr());
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glBindTexture(GL_TEXTURE_2D, 0); //dévérouillage

    if(!img->loadFromFile("rocket_motor.jpg")){
        return;
    }
    img->flipVertically();
    glGenTextures(1, &texReac);
    glBindTexture(GL_TEXTURE_2D, texReac);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img->getSize().x, img->getSize().y, 0,
            GL_RGBA, GL_UNSIGNED_BYTE, img->getPixelsPtr());
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glBindTexture(GL_TEXTURE_2D, 0); //dévérouillage
}
