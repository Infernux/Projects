#ifndef __VECTOR3D_H
#define __VECTOR3D_H

class Vector3D
{
    public:
        Vector3D();
        Vector3D(double x, double y, double z);

        void setX(double x);
        void setY(double y);
        void setZ(double z);

        double getX();
        double getY();
        double getZ();

    private:
        double x;
        double y;
        double z;
};
#endif
