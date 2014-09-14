#ifndef __COLOR_H
#define __COLOR_H

class Color {
    public:
        Color(int r=255, int g=255, int b=255);

        void setValues(int r, int g, int b);
        void setRed(int v);
        void setGreen(int v);
        void setBlue(int v);

        int getRed();
        int getGreen();
        int getBlue();

    private:
        int red;
        int green;
        int blue;
};

#endif
