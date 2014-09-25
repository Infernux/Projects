#ifndef __GAME_H
#define __GAME_H

#include <time.h>
#include <vector>

#include "const.h"
#include "Piece.h"

#define NB_PIECES 2
#include "Line.h"
#include "Square.h"

typedef struct structGrid{
    bool filled;
    int b;
}GridEl;

class Game {
    public:
        Game();
        void spawn(); //create a new activePiece
        void drawAll(GLUquadric*);

        std::vector<Piece*> fixedPieces;
        GridEl grid[WIDTH][HEIGHT];
        Piece *activePiece;

    private:
};

#endif
