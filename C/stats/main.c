#include <stdio.h>
#include <stdlib.h>
#include <math.h>

double mean(int count, double* values)
{
  int i = 0;
  double sum = 0;
  for(i = 0; i < count; ++i)
  {
    sum += values[i];
  }
  return sum/count;
}

double standardDeviation(int count, double* values)
{
  double stdmean = mean(count, values);

  int i = 0;
  double sum = 0.f;
  for(i = 0; i < count; ++i)
  {
    sum += pow((values[i] - stdmean), 2.f);
  }

  return sqrt(sum / (count - 1));
}

int readSize(FILE* fhandle)
{
  char buff[512];
  char c;
  if(fhandle)
  {
    int i=0;
    while((c = getc(fhandle)) != '\n' && c != EOF)
    {
      buff[i] = c;
      i++;
    }
    buff[i] = '\0';
  } else {
    perror("Error");
    exit(1);
  }
  return atoi(buff);
}

void readValues(FILE* fhandle, const int count, double* values)
{
  char buff[512];
  char c;
  if(fhandle)
  {
    int i=0, offset=0;
    while((c = getc(fhandle)) != EOF)
    {
      if(c == '\n')
      {
        buff[i] = '\0';
        i=0;
        values[offset] = atof(buff);
        printf("value %d : %f\n", offset, values[offset]);

        ++offset;
      } else {
        buff[i] = c;
        i++;
      }
    }
  } else {
    perror("Error");
    exit(1);
  }

}

int main(int argc, char** argv)
{
  FILE* fhandle = fopen(argv[1], "r");
  int count = readSize(fhandle);
  double *values = malloc(sizeof(double) * count);
  readValues(fhandle, count, values);

  printf("mean : %f\n", mean(count, values));
  printf("standard deviation : %f\n", standardDeviation(count, values));
  free(values);
}
