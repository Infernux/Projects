#include "file_readers.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "utils.h"

static uint8_t skipUntilNewLine(FILE *f);
static ImageStruct* readAsciiPpm(const char *path);
static ImageStruct* readBinaryPpm(const char *path);

ImageStruct* readPpm(const char *path)
{
  FILE *f = fopen(path, "r");
  if(!f) {
    printf("Couldn't open : %s\n", path);
    return NULL;
  }

  ImageStruct *imagestruct = NULL;

  char type[3];
  fread(type, sizeof(char), 2, f); /* try to fetch the type */
  if(strncmp(type, "P6", 2) == 0) {
    imagestruct = readBinaryPpm(path); /* TODO: pass the file pointer */
  } else if(strncmp(type, "P3", 2) == 0) {
    imagestruct = readAsciiPpm(path); /* TODO: pass the file pointer */
  } else {
    return NULL;
  }

  fclose(f);

  return imagestruct;
}

void skipComments(char *str, FILE *f)
{
  char bufskip;
  fgets(&bufskip, 1, f); /* fseek */

  if(bufskip == '#')
  {
    skipUntilNewLine(f);
  }
}

/* returns :
 *  > 0 when finding a new line
 *  -1 when not finding a new line
 * */
uint8_t skipUntilNewLine(FILE *f)
{
  char c='\0';
  while(((c=fgets(&c, 1, f)) != EOF) && (c != '\n'));
  return 0;
}

static ImageStruct* readAsciiPpm(const char *path)
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

  pst_return->p = malloc(sizeof(Pixel) * height * pitch);

  int x, y;
  for(y=0; y<height; ++y)
  {
    for(x=0; x<width; ++x)
    {
      pst_return->p[y*pitch + x].r = read_int(f);
      pst_return->p[y*pitch + x].g = read_int(f);
      pst_return->p[y*pitch + x].b = read_int(f);
    }
  }

  return pst_return;
}

static ImageStruct* readBinaryPpm(const char *path)
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

  pst_return->p = malloc(sizeof(Pixel) * height * pitch);

  fread(pst_return->p, sizeof(Pixel), height * pitch, f);

  return pst_return;
}

void freeImageStruct(ImageStruct *img_struct)
{
  free(img_struct->p);
  free(img_struct);
}
