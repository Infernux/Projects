#ifndef __CAMERA_H
#define __CAMERA_H

#include <SFML/Graphics.hpp>
#include <SFML/OpenGL.hpp>

class Camera
{
    public:
        Camera();
        void setCamera();
        void rotateLeft();
        void rotateRight();

        void moveLateralLeft();
        void moveLateralRight();
        void moveLateralUp();
        void moveLateralDown();

        void lookLeft();
        void lookRight();
        void lookUp();
        void lookDown();

    private:
        float X;
        float Y;
        float Z;

        float atX;
        float atY;
        float atZ;

        float angleZ;
};

#endif
