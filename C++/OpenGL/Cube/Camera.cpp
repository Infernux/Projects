#include "Camera.h"

Camera::Camera()
{
    X=5;
    Y=0;
    Z=3;
    atX=0;
    atY=0;
    atZ=0;
    angleZ=0;
}

void Camera::setCamera()
{
    glLoadIdentity();
    gluLookAt(X,Y,Z,atX,atY,atZ,0,0,1);
    //glTranslated(X, Y, Z);
    glRotatef(angleZ, 0.f, 0.f, 1.f);
}

void Camera::rotateLeft(){
    angleZ-=3.0f;
}

void Camera::rotateRight(){
    angleZ+=3.0f;
}

void Camera::lookLeft(){
    atX-=3.f;
}

void Camera::lookRight(){
    atX+=3.f;
}
