#include "interpolate.h"

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

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

/* modify so that the buffer is provided by the calling function */
uint8_t* addBorderToImage(const uint8_t *image, const int width, const int height, const int top_border, const int bottom_border, const int left_border, const int right_border)
{
  int new_stride = width + left_border + right_border;
  int new_height = height + top_border + bottom_border;
  uint8_t *output = (uint8_t*) malloc(sizeof(uint8_t) * new_stride * new_height);

  memset(output, 0, new_stride * new_height);

  int x, y, in_index;
  for(y=top_border; y < height + top_border; ++y)
  {
    for(x=left_border; x < width + left_border; ++x)
    {
      in_index = (y-top_border) * width + x - left_border;
      output[(y*new_stride) + x] = image[in_index];
    }
  }

  return output;
}

uint8_t* doubleImage(const uint8_t *image, const int width, const int height, const int stride)
{
  int new_stride = width * 2;
  int new_height = height * 2;
  uint8_t *output = (uint8_t*) malloc(sizeof(uint8_t) * new_stride * new_height);

  int x, y;
  int in_index, out_index;
  for(y=0; y<height; y++)
  {
    for(x=0; x<width; x++)
    {
      uint8_t v1, v2, v3, v4;
      in_index = (y * stride) + x;
      out_index= (y * 2 * new_stride) + x * 2;
      v1 = image[in_index];
      v2 = image[in_index + 1];
      v3 = image[in_index + stride];
      v4 = image[in_index + stride + 1];

      output[out_index]               = v1;
      output[out_index+1]             = (v1 + v2) / 2.;
      output[out_index+new_stride]    = (v1 + v3) / 2.;
      output[out_index+new_stride+1]  = (v1 + v4) / 2.;
    }
  }

  return output;
}

/* skip every other pixel */
uint8_t* halfImage_skip(const uint8_t *image, const int width, const int height, const int stride)
{
  int new_stride = width / 2;
  int new_height = height / 2;
  uint8_t *output = (uint8_t*) malloc(sizeof(uint8_t) * new_stride * new_height);

  int x, y;
  int in_index, out_index;
  for(y=0; y<height; y+=2)
  {
    for(x=0; x<width; x+=2)
    {
      int index = (y / 2.) * new_stride + x / 2.;
      output[index] = image[y * stride + x];
    }
  }

  return output;
}

uint8_t* halfImage_Linearish(const uint8_t *image, const int width, const int height, const int stride)
{
  int new_stride = width / 2;
  int new_height = height / 2;
  uint8_t *output = (uint8_t*) malloc(sizeof(uint8_t) * new_stride * new_height);

  int x, y;
  int in_index, out_index;
  for(y=0; y<height; y+=2)
  {
    for(x=0; x<width; x+=2)
    {
      uint8_t v1, v2, v3, v4;
      in_index = (y * stride) + x;
      out_index= (y / 2 * new_stride) + x / 2;
      v1 = image[in_index];
      v2 = image[in_index + 2];
      v3 = image[in_index + stride * 2];
      v4 = image[in_index + stride * 2 + 2];

      output[out_index] = (v1 + v2 + v3 + v4) / 4;
    }
  }

  return output;
}
