#ifndef __SQUARE_H
#define __SQUARE_H

#include <SFML/Graphics.hpp>
#include <SFML/OpenGL.hpp>
#include <iostream>

#include "Piece.h"

class Square : public Piece {
    public :
        Square();
        ~Square();
        
        void draw(GLUquadric*);
};

#endif
