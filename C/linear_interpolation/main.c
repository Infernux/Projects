#include <stdio.h>
#include <stdlib.h>

typedef struct point_
{
  float x;
  float y;
} Point;

void interpolate(Point *output, const Point *p1, const Point *p2)
{
  const float output_x = (p1->x + p2->x) / 2.;
  output->x = output_x;

  /* (y0(x1 - x) + y1(x - x0)) / (x1 - x0) */
  float y  = p1->y * (p2->x - output_x);
  y += p2->y * (output_x - p1->x);
  y /= p2->x - p1->x;

  output->y = y;
}

void printPoint(Point *p)
{
  printf("x : %f\n", p->x);
  printf("y : %f\n", p->y);
}

void main()
{
  printf("Pouet\n");

  Point p1 = {
    .x = 1,
    .y = 1
  };

  Point p2 = {
    .x = 2,
    .y = 2
  };

  Point output;

  interpolate(&output, &p1, &p2);

  printPoint(&output);
}
