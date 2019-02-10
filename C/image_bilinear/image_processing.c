#include "image_processing.h"

#include <stdio.h>
#include <stdlib.h>

int loadImage(const char *path, uint8_t *image, int *width, int *height, int *max_val)
{
  FILE *f = fopen(path, "rb");
  if(!f)
  {
    printf("Failed to open file : %s\n", path);
    return -1;
  }

  printf("File opened\n");

  //read header
  char buff[20];
  int char_count = 0;
  char cur_char;
  while(fread(&cur_char, sizeof(char), 1, f) && char_count < 20)
  {
    if(cur_char == '\n')
    {
      break;
    }

    buff[char_count] = cur_char;
    char_count++;
  }

  if(char_count == 20)
  {
    printf("Exited from %s at %d\n", __func__, __LINE__);
    return -1;
  }

  printf("File type : %s\n", buff);

  char_count = 0;

  while(fread(&cur_char, sizeof(char), 1, f) && char_count < 20)
  {
    if(cur_char == ' ')
    {
      buff[char_count] = '\0';
      break;
    }

    buff[char_count] = cur_char;
    char_count++;
  }

  if(char_count == 20)
  {
    printf("Exited from %s at %d\n", __func__, __LINE__);
    return -1;
  }

  *width = atoi(buff);

  char_count = 0;

  while(fread(&cur_char, sizeof(char), 1, f) && char_count < 20)
  {
    if(cur_char == '\n')
    {
      buff[char_count] = '\0';
      break;
    }

    buff[char_count] = cur_char;
    char_count++;
  }

  if(char_count == 20)
  {
    printf("Exited from %s at %d\n", __func__, __LINE__);
    return -1;
  }

  *height = atoi(buff);

  char_count = 0;

  while(fread(&cur_char, sizeof(char), 1, f) && char_count < 20)
  {
    if(cur_char == '\n')
    {
      buff[char_count] = '\0';
      break;
    }

    buff[char_count] = cur_char;
    char_count++;
  }

  if(char_count == 20)
  {
    printf("Exited from %s at %d\n", __func__, __LINE__);
    return -1;
  }

  *max_val = atoi(buff);

  printf("Read : %d\n", fread(image, sizeof(uint8_t), (*width) * (*height), f));

  fclose(f);
}

int saveAsTextPgm(const char *path, const uint8_t *image, const int width, const int height, const int max_val)
{
  FILE *f = fopen(path, "w");
  if(!f)
  {
    printf("Failed to open file : %s\n", path);
    return -1;
  }

  fprintf(f, "P2\n");
  fprintf(f, "%d %d\n", width, height);
  fprintf(f, "%d\n", max_val);

  unsigned int x, y;
  for(y=0; y<height; ++y)
  {
    for(x=0; x<width; ++x)
    {
      fprintf(f, "%03d ", image[(y * width) + x]);
    }
    fprintf(f, "\n");
  }

  fclose(f);
}
