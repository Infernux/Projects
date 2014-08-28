#include <iostream>
#include <vector>
#include <SFML/Graphics.hpp>
#include <SFML/System.hpp>
#include <typeinfo>

#include "Camera.h"

using namespace std;

int width, height;
float caseW, caseH;
Camera *camera;

//menu radial
void draw(){
    sf::ContextSettings ctxtSettings;
    ctxtSettings.depthBits = 32;

    sf::RenderWindow App(sf::VideoMode(800, 600), "Draxel", sf::Style::Default, ctxtSettings);
    width=800;
    height=600;
    caseW=width/10.f;
    caseH=height/10.f;

    //App.PreserveOpenGLStates(true);

    glDepthMask(GL_TRUE);
    glEnable(GL_DEPTH_TEST);

    glColor4f(1.f, 1.f, 1.f, 1.f);

    // Start game loop
    while (App.isOpen())
    {
        sf::Event event;
        while (App.pollEvent(event))
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
            }
            if(event.type == sf::Event::KeyPressed){
                switch(event.key.code)
                {
                    case sf::Keyboard::Up:
                        break;

                    case sf::Keyboard::Down:
                        break;

                    case sf::Keyboard::Left:
                        camera->rotateLeft();
                        break;

                    case sf::Keyboard::Right:
                        camera->rotateRight();
                        break;

                    case sf::Keyboard::Z:
                        break;

                    case sf::Keyboard::S:
                        break;

                    case sf::Keyboard::Q:
                        break;

                    case sf::Keyboard::D:
                        break;

                    case sf::Keyboard::I:
                        break;

                    case sf::Keyboard::K:
                        break;

                    case sf::Keyboard::J:
                        camera->rotateLeft();
                        break;

                    case sf::Keyboard::L:
                        camera->rotateRight();
                        break;

                    case sf::Keyboard::Escape:
                        return;

                    default:
                        break;
                }
            }
        }

        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();
        gluPerspective(70, (double)800/600, 1, 1000); //fov, ratio, près, loin

        // Clear depth buffer
        glClear(GL_COLOR_BUFFER_BIT);
        glMatrixMode(GL_MODELVIEW);
        
        camera->setCamera();

        //glRotatef(angleZ, 0.f, 0.f, 1.f);

        glBegin(GL_QUADS);
            glColor3ub(255, 0, 0);
            glVertex3d(1,1,1);
            glVertex3d(1,1,-1);
            glVertex3d(-1,1,-1);
            glVertex3d(-1,1,1);

            glColor3ub(0, 255, 0);
            glVertex3d(-1,1,1);
            glVertex3d(-1,1,-1);
            glVertex3d(-1,-1,-1);
            glVertex3d(-1,-1,1);

            glColor3ub(0, 0, 255);
            glVertex3d(1,1,1);
            glVertex3d(1,1,-1);
            glVertex3d(1,-1,-1);
            glVertex3d(1,-1,1);

            glColor3ub(255, 255, 0);
            glVertex3d(1,-1,1);
            glVertex3d(1,-1,-1);
            glVertex3d(-1,-1,-1);
            glVertex3d(-1,-1,1);

            glColor3ub(255, 0, 255); //top
            glVertex3d(1,1,1);
            glVertex3d(-1,1,1);
            glVertex3d(-1,-1,1);
            glVertex3d(1,-1,1);

            glColor3ub(255, 255, 255); //bottom
            glVertex3d(1,1,-1);
            glVertex3d(-1,1,-1);
            glVertex3d(-1,-1,-1);
            glVertex3d(1,-1,-1);
        glEnd();

        //App.Clear();
        glFlush();
        glClear(GL_DEPTH_BUFFER_BIT);

        //Finally, display the rendered frame on screen
        App.display();
    }
}

int main(){
    camera = new Camera();
    draw();
    delete camera;
    return 0; 
}
