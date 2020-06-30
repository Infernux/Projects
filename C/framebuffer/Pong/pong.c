#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <fcntl.h>
#include <linux/fb.h>
#include <sys/mman.h>
#include <sys/ioctl.h>

#define ballHalfSize 10
#define STEP 1

typedef struct strBall{
    int x;
    int y;
    int sensX, sensY;
} Ball;

typedef struct strScreenInfos{
    int fbfd;
    char *fbp;
    char *fbpBack;
    struct fb_var_screeninfo vinfo;
    struct fb_fix_screeninfo finfo;
    char flip;
} ScreenInfos;

void swapBuffers(ScreenInfos* si){
    si->vinfo.yoffset=(si->flip==0?0:1050);
    ioctl(si->fbfd, FBIOPUT_VSCREENINFO, si->vinfo);

    char* tmp = si->fbp;
    si->fbp=si->fbpBack;
    si->fbpBack=tmp;
    si->flip=!si->flip;
}

//minimum size of a number is 3 pixels wide and 5 pixels high
void drawNumber(ScreenInfos* si, int x, int y, int number){
    switch(number){
        case 0:
            break;

        case 1:
            break;

        default:
            break;
    }
}

void drawPixel(ScreenInfos* si, int x, int y, char red, char green, char blue, char alpha){
    long int location = (x+si->vinfo.xoffset) * (si->vinfo.bits_per_pixel/8) +
        (y+si->vinfo.yoffset) * si->finfo.line_length;

    if (si->vinfo.bits_per_pixel == 32) {
        *(si->fbpBack + location) = blue;        // Some blue
        *(si->fbpBack + location + 1) = green;     // A little green
        *(si->fbpBack + location + 2) = red;    // A lot of red
        *(si->fbpBack + location + 3) = 255;      // No transparency
        //location += 4;
    } else  { //assume 16bpp
        int b = 10;
        int g = (x-100)/6;     // A little green
        int r = 31-(y-100)/16;    // A lot of red
        unsigned short int t = r<<11 | g << 5 | b;
        *((unsigned short int*)(si->fbpBack + location)) = t;
    }
}

void smartBlit(ScreenInfos* si, Ball* ball){
    long int location;
    int x, y;
    for (y = ball->y-ballHalfSize; y < ball->y+ballHalfSize; y++){
        for (x = ball->x-ballHalfSize; x < ball->x+ballHalfSize; x++) {
            drawPixel(si, x, y, 123, 0, 0, 255);
        }
    }
}

void blit(ScreenInfos* si){
    int x, y;
    for (y = 0; y < si->vinfo.yres; y++){
        for (x = 0; x < si->vinfo.xres; x++) {
            drawPixel(si, x, y, 123, 0, 0, 255);
        }
    }
    
}

void fullblit(ScreenInfos* si){
    long int location;
    int x, y;
    //*2 to redraw the buffer
    for (y = 0; y < si->vinfo.yres*2; y++){
        for (x = 0; x < si->vinfo.xres; x++) {
            long int location = (x+si->vinfo.xoffset) * (si->vinfo.bits_per_pixel/8) +
                (y+si->vinfo.yoffset) * si->finfo.line_length;
            *(si->fbp + location) = 0;        // Some blue
            *(si->fbp + location + 1) = 0;     // A little green
            *(si->fbp + location + 2) = 123;    // A lot of red
            *(si->fbp + location + 3) = 255;      // No transparency
        }
    }
}

int main()
{
    ScreenInfos si;
    long int screensize = 0;
    int x = 0, y = 0;
    long int location = 0;

    si.flip=0;

    Ball ball;
    ball.x=200;
    ball.y=300;
    ball.sensY=1;
    ball.sensX=1;

    // Open the file for reading and writing
    si.fbfd = open("/dev/fb0", O_RDWR);
    if (si.fbfd == -1) {
        perror("Error: cannot open framebuffer device");
        exit(1);
    }

    // Get fixed screen information
    if (ioctl(si.fbfd, FBIOGET_FSCREENINFO, &si.finfo) == -1) {
        perror("Error reading fixed information");
        exit(2);
    }

    // Get variable screen information
    if (ioctl(si.fbfd, FBIOGET_VSCREENINFO, &si.vinfo) == -1) {
        perror("Error reading variable information");
        exit(3);
    }

    printf("%dx%d, %dbpp\n", si.vinfo.xres, si.vinfo.yres, si.vinfo.bits_per_pixel);

    // Figure out the size of the screen in bytes
    screensize = si.vinfo.xres * si.vinfo.yres * si.vinfo.bits_per_pixel / 8;

    // Map the device to memory
    si.fbp = (char *)mmap(0, screensize*2, PROT_READ | PROT_WRITE, MAP_SHARED, si.fbfd, 0);
    if ((int)si.fbp == -1) {
        perror("Error: failed to map framebuffer device to memory");
        exit(4);
    }

    si.fbpBack = si.fbp + screensize;

    // Figure out where in memory to put the pixel
    fullblit(&si);
    swapBuffers(&si);

    while(1){
        int x, y;
        for(y=ball.y-ballHalfSize; y<ball.y+ballHalfSize; ++y){
            for(x=ball.x-ballHalfSize; x<ball.x+ballHalfSize; ++x){
                drawPixel(&si, x, y, 255, 255, 255, 255);
            }
        }
        swapBuffers(&si);
        blit(&si);
        usleep(5000);
    //printf("Test\n");


        ball.y+=STEP*ball.sensY;
        ball.x+=STEP*ball.sensX;

        if(ball.y>=si.vinfo.yres-ballHalfSize){
            ball.sensY=-1;
            ball.y=si.vinfo.yres-ballHalfSize-1;
        }
        if(ball.y<ballHalfSize){
            ball.sensY=1;
            ball.y=ballHalfSize;
        }
        if(ball.x>=si.vinfo.xres-ballHalfSize){
            ball.sensX=-1;
            ball.x=si.vinfo.xres-ballHalfSize-1;
        }
        if(ball.x<ballHalfSize){
            ball.sensX=1;
            ball.x=ballHalfSize;
        }
    }
    munmap(si.fbp, screensize*2);
    close(si.fbfd);
    return 0;
}
