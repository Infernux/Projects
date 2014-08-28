#ifndef __BALL_H
#define __BALL_H

#include <SFML/Graphics.hpp>
#include <SFML/OpenGL.hpp>

#include <iostream>

class Ball {
    public:
        Ball();
        void draw(GLUquadric*);
        void setColor(int r, int g, int b);

        void reset();
        void move(float time);
        void invertH();

        float getZ();
        float getX();
        void setX(int val);
        
    private:
        float z;
        float x;

        bool sensV;
        bool sensH;
        
        int red;
        int green;
        int blue;
};

#endif
