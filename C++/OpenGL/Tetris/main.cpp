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
#include "HUD.h"
#include "const.h"
#include "Game.h"

using namespace std;

float caseW, caseH;
Camera *camera;
Game game;

KeyboardManager kbmg;

int counter = 0;
int height = WINDOW_HEIGHT, width = WINDOW_WIDTH;

void draw(sf::RenderWindow *App, GLfloat *LightAmbient, GLfloat *LightDiffuse, GLfloat *lightpos, sf::Vector2i last);

//menu radial

void mainLoop(sf::RenderWindow *app){
    //éclairage
    GLfloat LightAmbient[] = {.5f, .5f, .5f, 1.f};
    GLfloat LightDiffuse[] = {1.f, 1.f, 1.f, 1.f};
    GLfloat lightpos[] = {-5.f, 0.f, 0.f, 1.f};

    sf::Vector2i last = sf::Vector2i(WINDOW_WIDTH/2, WINDOW_HEIGHT/2);

    while (app->isOpen())
    {
        draw(app, LightAmbient, LightDiffuse, lightpos, last);
    }
}

void draw(sf::RenderWindow *App, GLfloat *LightAmbient, GLfloat *LightDiffuse, GLfloat *lightpos, sf::Vector2i last){
    sf::Clock clock;

    // Start game loop
    glLoadIdentity();
    gluPerspective(70, (double)(WINDOW_WIDTH/WINDOW_HEIGHT), 1, 1000); //fov, ratio, près, loin
    GLUquadric* params;
    params=gluNewQuadric();

    sf::Event event;
    while(App->pollEvent(event))
    {
        // Close window : exit
        if (event.type == sf::Event::Closed)
            App->close();
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
                    App->close();
                    return;

                default:
                    break;
            }
        }
    }

    /*sf::Vector2i act = sf::Mouse::getPosition();
      if(act!=last){
      camera->rotateMouse(last-act);
      sf::Mouse::setPosition(last, App->;
      }*/

    float elapsed = clock.getElapsedTime().asSeconds()*3000;
    kbmg.getInputs(App);
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
    counter += clock.getElapsedTime().asMilliseconds();

    drawArena();
    game.drawAll(params);

    //App->Clear();
    glFlush();

    //Finally, display the rendered frame on screen
    App->display();
    gluDeleteQuadric(params);

    clock.restart();
}

sf::RenderWindow* initWindow(){
    sf::ContextSettings ctxtSettings;
    ctxtSettings.depthBits = 32;

    sf::RenderWindow *App = new sf::RenderWindow(sf::VideoMode(WINDOW_WIDTH, WINDOW_HEIGHT), "Tetrix", sf::Style::Default, ctxtSettings);
    //sf::RenderWindow Appsf::VideoMode(WINDOW_WIDTH, WINDOW_HEIGHT), "Tetrix", sf::Style::Fullscreen, ctxtSettings);
    App->setVerticalSyncEnabled(true);
    App->setActive();

    caseW=WINDOW_WIDTH/10.f;
    caseH=WINDOW_HEIGHT/10.f;

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

    return App;
}

int main(){
    camera = new Camera();

    sf::RenderWindow* app = initWindow();
    mainLoop(app);

    delete app;
    delete camera;
    return 0; 
}
