#include "Game.h"

Game::Game(){
    srand(time(NULL));
}

void Game::spawn(){
    Piece *newActive=NULL;
    switch(rand() % NB_PIECES){
        case 0:
            newActive = new Square();
            break;

        case 1:
            newActive = new Line();
            break;
    }
    activePiece = newActive;
}

void Game::drawAll(GLUquadric *params){
    activePiece->draw(params);
    for(std::vector<Piece*>::iterator it = fixedPieces.begin(); it!=fixedPieces.end(); it++){
        (*it)->draw(params);
    }
}
