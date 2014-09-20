#ifndef __LINE_H
#define __LINE_H

#include <SFML/Graphics.hpp>
#include <SFML/OpenGL.hpp>
#include <iostream>

#include "Piece.h"

class Line : public Piece {
    public :
        Line();
        ~Line();
        
        void draw(GLUquadric*);
};

#endif
