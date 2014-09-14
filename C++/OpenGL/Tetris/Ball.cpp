#include "Ball.h"

Ball::Ball(){
    z=0;
    x=5;

    sensV = true;
    sensH = true;

    red = 0;
    green = 100;
    blue = 255;
}

void Ball::setColor(int r, int g, int b){
    red = r;
    green = g;
    blue = b;
}

void Ball::draw(GLUquadric *params){
    glColor3ub(red, green, blue);
    glPushMatrix();
    glTranslated(x, 0, z);
    glBegin(GL_QUADS);
        //left
        glNormal3f(-1.f, 0.f, 0.f);
        glVertex3d(-1, 1, -1);
        glVertex3d(-1, 1, 1);
        glVertex3d(-1, -1, 1);
        glVertex3d(-1, -1, -1);

        //back
        glNormal3f(0.f, -1.f, 0.f);
        glVertex3d(-1, -1, -1);
        glVertex3d(-1, -1, 1);
        glVertex3d(1, -1, 1);
        glVertex3d(1, -1, -1);

        //right
        glNormal3f(1.f, 0.f, 0.f);
        glVertex3d(1, -1, -1);
        glVertex3d(1, -1, 1);
        glVertex3d(1, 1, 1);
        glVertex3d(1, 1, -1);

        //front
        glNormal3f(0.f, 1.f, 0.f);
        glVertex3d(-1, 1, -1);
        glVertex3d(-1, 1, 1);
        glVertex3d(1, 1, 1);
        glVertex3d(1, 1, -1);

        //top
        glNormal3f(0.f, 0.f, 1.f);
        glVertex3d(-1, 1, 1);
        glVertex3d(-1, -1, -1);
        glVertex3d(1, -1, -1);
        glVertex3d(1, 1, -1);

        //bottom
        glNormal3f(0.f, 0.f, -1.f);
        glVertex3d(-1, 1, -1);
        glVertex3d(-1, -1, -1);
        glVertex3d(1, -1, -1);
        glVertex3d(1, 1, -1);
    glEnd();
    glPopMatrix();
}

void Ball::reset(){
    z = 0;
    x = 0;
}

void Ball::invertH(){
    sensH=!sensH;   
}

float Ball::getX(){
    return x;
}

float Ball::getZ(){
    return z;
}

void Ball::setX(int val){
    x = val;
}

void Ball::move(float time){
    x += sensH?time:-time;
    z += sensV?time:-time;

    if(x>9){
        reset();
    }else if(x<-9){
        reset();
    }

    if(z>11){
        z=11;
        sensV=!sensV;
    }else if(z<-11){
        z=-11;
        sensV=!sensV;
    }
}
