#include "HUD.h"

void drawArena(){
    glPushMatrix();
    glColor3ub(255, 255, 0);
    glBegin(GL_QUADS);

    //bottom
    glVertex3d(-WIDTH,1,-HEIGHT);
    glVertex3d(-WIDTH,-1,-HEIGHT);
    glVertex3d(WIDTH,-1,-HEIGHT);
    glVertex3d(WIDTH,1,-HEIGHT);

    //left
    glVertex3d(-WIDTH,-1,-HEIGHT);
    glVertex3d(-WIDTH,-1,HEIGHT);
    glVertex3d(-WIDTH,1,HEIGHT);
    glVertex3d(-WIDTH,1,-HEIGHT);

    //top
    glVertex3d(-WIDTH,1,HEIGHT);
    glVertex3d(-WIDTH,-1,HEIGHT);
    glVertex3d(WIDTH,-1,HEIGHT);
    glVertex3d(WIDTH,1,HEIGHT);

    //right
    glVertex3d(WIDTH,1,HEIGHT);
    glVertex3d(WIDTH,-1,HEIGHT);
    glVertex3d(WIDTH,-1,-HEIGHT);
    glVertex3d(WIDTH,1,-HEIGHT);

    glEnd();
    glPopMatrix();
}
