#include "Camera.h"

Camera::Camera()
{
    X=10;
    Y=0;
    Z=0;
    angleV=0;
    angleH=180;
    mvmtSpeed=.1f;
    rotateSpeed=2;
}

void Camera::moveBackward(float elapsed){
    X-=direction.X*mvmtSpeed*elapsed;
    Y-=direction.Y*mvmtSpeed*elapsed;
    Z-=direction.Z*mvmtSpeed*elapsed;
}

void Camera::moveForward(float elapsed){
    X+=direction.X*mvmtSpeed*elapsed;
    Y+=direction.Y*mvmtSpeed*elapsed;
    Z+=direction.Z*mvmtSpeed*elapsed;
}

void Camera::moveLateralLeft(float elapsed){
    float newAngle = angleH+90.f;
    X += cos(newAngle*conv)*mvmtSpeed*elapsed;
    Y += sin(newAngle*conv)*mvmtSpeed*elapsed;
}

void Camera::moveLateralRight(float elapsed){
    float newAngle = angleH-90.f;
    X += cos(newAngle*conv)*mvmtSpeed*elapsed;
    Y += sin(newAngle*conv)*mvmtSpeed*elapsed;
}

void Camera::lookUp(float elapsed){
    if(angleV<90){
        angleV+=rotateSpeed;
    }else{
        angleV = 90;
    }
}

void Camera::lookDown(float elapsed){
    if(angleV>-90){
        angleV-=rotateSpeed;
    }else{
        angleV=-90;
    }
}

void Camera::lookLeft(float elapsed){
    //if(angleH<90){
        angleH+=rotateSpeed;
    //}
}

void Camera::lookRight(float elapsed){
    //if(angleH>-90){
        angleH-=rotateSpeed;
    //}
}

void Camera::rotateMouse(sf::Vector2i move){
    angleH+=move.x;
    angleV+=move.y;
    if(angleV>90){
        angleV = 90;
    }else if(angleV<-90){
        angleV = -90;
    }
}

void Camera::setCamera()
{
    direction.X = cos(angleH*conv)*cos(angleV*conv);
    direction.Y = sin(angleH*conv)*cos(angleV*conv);
    direction.Z = sin(angleV*conv);

    gluLookAt(X,Y,Z,X+direction.X,Y+direction.Y,Z+direction.Z,0,0,1);
    //gluLookAt(X,Y,Z,0,0,0,0,0,1);
    std::cout << "X :" << X << " Y :" << Y << " Z:" << Z << std::endl;
}

void Camera::rotateLeft(){
}

void Camera::rotateRight(){
}

void Camera::rotateUp(){
    angleV-=1.f;
}

void Camera::rotateDown(){
    angleV+=1.f;
}
