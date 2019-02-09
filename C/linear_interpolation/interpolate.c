#include "interpolate.h"

#include <stdio.h>

void interpolate(Point *output, const Point *p1, const Point *p2)
{
  if(p2->x - p1->x != 0)
  {
    const float output_x = (p1->x + p2->x) / 2.;
    output->x = output_x;

    /* (y0(x1 - x) + y1(x - x0)) / (x1 - x0) */
    float y  = p1->y * (p2->x - output_x);
    y += p2->y * (output_x - p1->x);

    y /= p2->x - p1->x;
    output->y = y;
  } else {
    const float output_y = (p1->y + p2->y) / 2.;
    output->y = output_y;
    output->x = 0;
  }
}

void printPoint(Point *p)
{
  printf("x : %f\n", p->x);
  printf("y : %f\n", p->y);
}
