#include "file_readers.h"

#include <stdio.h>
#include <stdlib.h>

#include "utils.h"

void skipComments(char *str, FILE *f)
{
  char bufskip[50];
  fgets(bufskip, 50, f); /* fseek */

  if(bufskip[0] == '#')
  {
    skipUntilNewLine(f);
  }
}

/* returns :
 *  > 0 when finding a new line
 *  -1 when not finding a new line
 * */
uint8_t skipUntilNewLine(char *str, uint32_t buffer_size)
{
  for(int i=0; i < 5- 
}

ImageStruct* readAsciiPpm(char *path)
{
  FILE *f = fopen(path, "r");
  ImageStruct* pst_return = malloc(sizeof(ImageStruct));

  char bufskip[50];
  fgets(bufskip, 50, f); /* fseek */



  int width = read_int(f);
  int height = read_int(f);
  int pitch = width;
  int max = read_int(f);

  printf("height : %d, width : %d\n", height, width);

  pst_return->width = width;
  pst_return->height = height;
  pst_return->pitch = width;

  pst_return->r = malloc(sizeof(uint8_t) * height * pitch);
  pst_return->g = malloc(sizeof(uint8_t) * height * pitch);
  pst_return->b = malloc(sizeof(uint8_t) * height * pitch);

  int index = 0;

  int x, y;
  for(y=0; y<height; ++y)
  {
    for(x=0; x<width; ++x)
    {
      pst_return->r[y*pitch + x] = read_int(f);
      pst_return->g[y*pitch + x] = read_int(f);
      pst_return->b[y*pitch + x] = read_int(f);
    }
  }

  return pst_return;
}

void freeImageStruct(ImageStruct *img_struct)
{
  free(img_struct->r);
  free(img_struct->g);
  free(img_struct->b);
  free(img_struct);
}
