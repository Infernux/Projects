#ifndef __COORD_H
#define __COORD_H

class Coord {
    public:
        Coord(int x=0, int y=0);
        int getX();
        int getY();
        void setCoord(int x, int y);
        void setX(int x);
        void setY(int y);

        bool alive;

    private:
        int x, y;
};

#endif
