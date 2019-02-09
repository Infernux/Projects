#ifndef INTERPOLATE_H__
#define INTERPOLATE_H__

typedef struct point_
{
  float x;
  float y;
} Point;

void interpolate(Point *output, const Point *p1, const Point *p2);
void printPoint(Point *p);

#endif /* INTERPOLATE_H__ */
