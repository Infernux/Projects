#ifndef FILE_READERS_H__
#define FILE_READERS_H__

#include <inttypes.h>

typedef struct pixel_
{
  uint8_t r;
  uint8_t g;
  uint8_t b;
} Pixel;

typedef struct imagestruct_
{
  int width;
  int height;
  int pitch;

  Pixel *p;
} ImageStruct;

ImageStruct* readPpm(const char *path);

void freeImageStruct(ImageStruct *img_struct);

#endif /* FILE_READERS_H__ */
