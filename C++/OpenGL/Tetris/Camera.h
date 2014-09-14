#ifndef __CAMERA_H
#define __CAMERA_H

#include <SFML/Graphics.hpp>
#include <SFML/OpenGL.hpp>
#include <cmath>

#include <iostream>

#include "Vector3D.h"

#define PI 3.141592f

class Camera
{
    public:
        Camera();
        void setCamera();
        void rotateLeft();
        void rotateRight();
        void rotateUp();
        void rotateDown();
        void rotateMouse(sf::Vector2i move);

        void moveLateralLeft(float elapsed);
        void moveLateralRight(float elapsed);
        void moveLateralUp(float elapsed);
        void moveLateralDown(float elapsed);

        void lookLeft(float elapsed);
        void lookRight(float elapsed);
        void lookUp(float elapsed);
        void lookDown(float elapsed);

        void moveForward(float elapsed);
        void moveBackward(float elapsed);
    private:
        static const float conv = PI/180.f;

        Vector3D direction;
        float mvmtSpeed;
        float rotateSpeed;

        float X;
        float Y;
        float Z;

        float angleH;
        float angleV;
};

#endif
