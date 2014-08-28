#ifndef __PAD_H
#define __PAD_H

#include <SFML/Graphics.hpp>
#include <SFML/OpenGL.hpp>

class Pad {
    public:
        Pad();
        ~Pad();
        void draw(GLUquadric*);
        void setColor(int r, int g, int b);
        void setX(int newX);
        float getZ();

        void up(float elapsed);
        void down(float elapsed);

    private:
        void loadTextures();

        sf::Image *img;
        GLuint texTop;
        GLuint texMiddle;
        GLuint texBot;
        GLuint texReac;

        float height;

        float z;
        float x;
        
        int red;
        int green;
        int blue;
};

#endif
