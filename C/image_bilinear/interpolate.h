#ifndef INTERPOLATE_H__
#define INTERPOLATE_H__

#include <stdint.h>

typedef struct point_
{
  float x;
  float y;
} Point;

void interpolate(Point *output, const Point *p1, const Point *p2);
void printPoint(Point *p);

uint8_t* addBorderToImage(const uint8_t *image, const int width, const int height, const int top_border, const int bottom_border, const int left_border, const int right_border);
uint8_t* doubleImage(const uint8_t *image, const int width, const int height, const int stride);

#endif /* INTERPOLATE_H__ */
