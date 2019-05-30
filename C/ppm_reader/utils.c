#include "utils.h"

#include <stdlib.h>

int read_int(FILE *f)
{
  char reader;
  char buf[50];
  int current_index = 0;

  if(feof(f))
    return -1;

  while(fread(&reader, sizeof(char), 1, f))
  {
    if(current_index > 49)
    {
      return -1;
    }

    if(reader == ' ' || reader == '\n' || reader == '\r')
    {
      if(current_index != 0)
      {
        buf[current_index] = '\0';
        break;
      }
    }

    buf[current_index] = reader;
    current_index++;
  }

  return atoi(buf);
}
