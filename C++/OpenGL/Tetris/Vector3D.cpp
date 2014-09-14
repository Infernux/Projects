#include "Vector3D.h"

Vector3D::Vector3D(){

}

Vector3D::Vector3D(double x, double y, double z){
    this->x=x;
    this->y=y;
    this->z=z;
}

void Vector3D::setX(double x){
    this->x=x;
}

void Vector3D::setY(double y){
    this->y=y;
}

void Vector3D::setZ(double z){
    this->z=z;
}

double Vector3D::getX(){
    return x;
}

double Vector3D::getY(){
    return y;
}

double Vector3D::getZ(){
    return z;
}
