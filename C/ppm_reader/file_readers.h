#ifndef FILE_READERS_H__
#define FILE_READERS_H__

#include <inttypes.h>

typedef struct imagestruct_
{
  int width;
  int height;
  int pitch;

  uint8_t *r;
  uint8_t *g;
  uint8_t *b;
} ImageStruct;

ImageStruct* readAsciiPpm(char *path);

void freeImageStruct(ImageStruct *img_struct);

#endif /* FILE_READERS_H__ */
