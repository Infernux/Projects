#include <iostream>
#include <vector>
#include <SFML/Graphics.hpp>
#include <SFML/System.hpp>
#include <SFML/OpenGL.hpp>

#include <typeinfo>

#include "Camera.h"
#include "Pad.h"
#include "Square.h"
#include "Line.h"
#include "KeyboardManager.h"

using namespace std;

float caseW, caseH;
Camera *camera;
Square square;
Line line;

KeyboardManager kbmg;

int width = 1366;
int height = 768;

//menu radial
void draw(){
    //éclairage
    GLfloat LightAmbient[] = {.5f, .5f, .5f, 1.f};
    GLfloat LightDiffuse[] = {1.f, 1.f, 1.f, 1.f};
    GLfloat lightpos[] = {-5.f, 0.f, 0.f, 1.f};

    sf::ContextSettings ctxtSettings;
    ctxtSettings.depthBits = 32;

    sf::Vector2i last = sf::Vector2i(width/2, height/2);

    //sf::RenderWindow App(sf::VideoMode(width, height), "Draxel", sf::Style::Default, ctxtSettings);
    sf::RenderWindow App(sf::VideoMode(width, height), "Tetrix", sf::Style::Fullscreen, ctxtSettings);
    App.setVerticalSyncEnabled(true);
    App.setActive();

    caseW=width/10.f;
    caseH=height/10.f;

    glDepthMask(GL_TRUE);
    glEnable(GL_DEPTH_TEST);
    glShadeModel(GL_SMOOTH);
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST);
    /*glLightfv(GL_LIGHT1, GL_AMBIENT, LightAmbient);
    glLightfv(GL_LIGHT1, GL_DIFFUSE, LightDiffuse);
    glLightfv(GL_LIGHT1, GL_POSITION, lightpos);*/

    /*glEnable(GL_LIGHT1);
    glEnable(GL_LIGHTING);*/

    glColor4f(1.f, 1.f, 1.f, 1.f);

    glEnable(GL_TEXTURE_2D);
    glMatrixMode(GL_PROJECTION);
    glClearDepth(1.f);

    sf::Clock clock;

    // Start game loop
    while (App.isOpen())
    {
        glLoadIdentity();
        gluPerspective(70, (double)(width/height), 1, 1000); //fov, ratio, près, loin
        GLUquadric* params;
        params=gluNewQuadric();

        sf::Event event;
        while(App.pollEvent(event))
        {
            // Close window : exit
            if (event.type == sf::Event::Closed)
                App.close();
            if (event.type == sf::Event::Resized){
                glViewport(0, 0, event.size.width, event.size.height);
                width=event.size.width;
                height=event.size.height;
                caseW=width/10.f;
                caseH=height/10.f;
                last = sf::Vector2i(width/2, height/2);
            }

            if(event.type == sf::Event::KeyPressed){
                switch(event.key.code)
                {
                    case sf::Keyboard::Escape:
                        gluDeleteQuadric(params);
                        return;

                    default:
                        break;
                }
            }
        }

        /*sf::Vector2i act = sf::Mouse::getPosition();
        if(act!=last){
            camera->rotateMouse(last-act);
            sf::Mouse::setPosition(last, App);
        }*/

        float elapsed = clock.getElapsedTime().asSeconds()*3000;
        kbmg.getInputs(&App);
        if(kbmg.up){
            camera->lookUp(1.f);
        }
        if(kbmg.left){
            camera->lookLeft(1.f);
        }
        if(kbmg.down){
            camera->lookDown(1.f);
        }
        if(kbmg.right){
            camera->lookRight(1.f);
        }
        if(kbmg.backward){
            camera->moveBackward(1.f);
        }
        if(kbmg.forward){
            camera->moveForward(1.f);
        }
        if(kbmg.strafeLeft){
            camera->moveLateralLeft(1.f);
        }
        if(kbmg.strafeRight){
            camera->moveLateralRight(1.f);
        }
        //ajouter le temps =)

        // Clear depth buffer
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT);
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();

        gluQuadricTexture(params, GL_TRUE);

        camera->setCamera();
        /*lightpos[0]=ball.getX();
        lightpos[2]=ball.getZ();*/
        //glLightfv(GL_LIGHT1, GL_POSITION, lightpos);

//        square.draw(params);
        line.draw(params);

        //terrain
        glPushMatrix();
        glColor3ub(255, 255, 0);
        glBegin(GL_QUADS);
        //outter
            //bottom
            glVertex3d(-15,1,-15);
            glVertex3d(-15,-1,-15);
            glVertex3d(15,-1,-15);
            glVertex3d(15,1,-15);

            //left
            glVertex3d(-15,-1,-15);
            glVertex3d(-15,-1,15);
            glVertex3d(-15,1,15);
            glVertex3d(-15,1,-15);

            //top
            glVertex3d(-15,1,15);
            glVertex3d(-15,-1,15);
            glVertex3d(15,-1,15);
            glVertex3d(15,1,15);

            //right
            glVertex3d(15,1,15);
            glVertex3d(15,-1,15);
            glVertex3d(15,-1,-15);
            glVertex3d(15,1,-15);

        //inner
            //bottom
            glVertex3d(-12,1,-12);
            glVertex3d(-12,-1,-12);
            glVertex3d(12,-1,-12);
            glVertex3d(12,1,-12);

            //left
            glVertex3d(-12,-1,-12);
            glVertex3d(-12,-1,12);
            glVertex3d(-12,1,12);
            glVertex3d(-12,1,-12);

            //top
            glVertex3d(-12,1,12);
            glVertex3d(-12,-1,12);
            glVertex3d(12,-1,12);
            glVertex3d(12,1,12);

            //right
            glVertex3d(12,1,12);
            glVertex3d(12,-1,12);
            glVertex3d(12,-1,-12);
            glVertex3d(12,1,-12);
        glEnd();
        glPopMatrix();

        //App.Clear();
        glFlush();

        //Finally, display the rendered frame on screen
        App.display();
        gluDeleteQuadric(params);

        clock.restart();
    }
}

int main(){
    camera = new Camera();
    draw();
    delete camera;
    return 0; 
}
