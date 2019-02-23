#include <stdio.h>
#include <iostream>
#include <math.h>
#include <string.h>

#include "filters.h"
#include "unravel_convol.h"
#include "naive_convol.h"
#include "dual_convol.h"
#include "triple_convol.h"
#include "linear_convol.h"
#include "convol.h"
#include "common.h"

#ifdef USE_CIMG
#include "CImg.h"
#endif /* USE_CIMG */

#define Kr 0.299
#define Kg 0.587
#define Kb 0.114

#define WRITE_DOWN

#ifdef USE_CIMG
using namespace cimg_library;
#endif /* USE_CIMG */
using namespace std;

void print_timediff(struct timespec *start, struct timespec *end)
{
  int s = end->tv_sec - start->tv_sec;
  int ns = end->tv_nsec - start->tv_nsec;
  cout << s * 1000 + ns / 1000000 << "ms" << endl;
}

uint8_t* zero_pad(uint8_t* mat, int width, int height, int padding);

#ifdef USE_CIMG
double* RGBSpaceToYCrCm(CImg<double> *img)
{
  double* out = new double[img->width() * img->height()];

  for(int j=0; j<img->height(); ++j)
  {
    for(int i=0; i<img->width(); ++i)
    {
      double red = (*img)(i, j, 0);
      double green = (*img)(i, j, 1);
      double blue = (*img)(i, j, 2);

      out[i+j*img->width()] = Kr*red + Kg*green + Kb*blue;
      //double Pb = 0.5f * (blue - Y)/(1-Kb);
      //double Pr = 0.5f * (red - Y)/(1-Kr);
    }
  }

  return out;
}

void YCrCmSpaceToRGB(CImg<double>* d, double* img, int padding, int width, int height)
{
  for(int y=0 + padding; y<height + padding; ++y)
  {
    for(int x=0 + padding; x<width + padding; ++x)
    {
      int Y = img[x + y * (width+padding*2)];
      (*d)(x-padding, y-padding,0) = Y;
      (*d)(x-padding, y-padding,1) = Y;
      (*d)(x-padding, y-padding,2) = Y;
    }
  }
}

#endif /* USE_CIMG */

void write_down_img(uint8_t* buffer, char* output, const int width, const int height)
{
  bool binary = 1;
  FILE *f = fopen(output, "wb");
  if(!f)
  {
    printf("Couldn't open file %s\n", output);
  }
  fprintf(f, "%s\n%d %d\n255\n", binary?"P5" : "P2", width, height);

  //YCrCmSpaceToRGB(&img, buffer, 0, width, height);
  if(binary)
  {
    fwrite(buffer, sizeof(uint8_t), width*height, f);
  } else {
    for(int j=0; j<height; ++j)
    {
      for(int i=0; i<width; ++i)
      {
        fprintf(f, "%03d ", buffer[j*width + i]);
      }
      fprintf(f, "\n");
    }
  }

  fclose(f);
}

uint8_t* loadPgm(const char *path, int *width, int *height)
{
  FILE *f = fopen(path, "rb");
  if(f==NULL)
    return NULL;

  char c;
  char buff[50];
  int count = 0;
  while(fread(&c, sizeof(uint8_t), 1, f) && c!='\n')
  {
    buff[count] = c;
    count++;
  }
  buff[count] = '\0';
  printf("Header %s\n", buff);

  count = 0;
  while(fread(&c, sizeof(uint8_t), 1, f) && c!=' ')
  {
    buff[count] = c;
    count++;
  }
  buff[count] = '\0';
  printf("w %s\n", buff);

  *width = atoi(buff);

  count = 0;
  while(fread(&c, sizeof(uint8_t), 1, f) && c!='\n')
  {
    buff[count] = c;
    count++;
  }
  buff[count] = '\0';
  printf("h %s\n", buff);

  *height = atoi(buff);

  count = 0;
  while(fread(&c, sizeof(uint8_t), 1, f) && c!='\n')
  {
    buff[count] = c;
    count++;
  }
  buff[count] = '\0';
  printf("max %s\n", buff);

  uint8_t* output = (uint8_t*) malloc(sizeof(uint8_t) * (*width) * (*height));
  fread(output, sizeof(uint8_t), (*width) * (*height), f);

  fclose(f);
  return output;
}

uint8_t* measure_convol(Convol *fa, uint8_t *img_org, Filter filter, int width, int height)
{
  fa->whatIsMyName();

  int padding = 1;
  uint8_t* padded_img = zero_pad(img_org,width,height,padding);

  struct timespec start, end;
  clock_gettime(CLOCK_MONOTONIC, &start);

  fa->apply_filter(img_org, padded_img, filter, width, height, padding);

  clock_gettime(CLOCK_MONOTONIC, &end);
  print_timediff(&start, &end);

  free(padded_img);

  return img_org;
}

bool compareImgs(double* a, double* b, int width, int height)
{
  for(int y=0; y<height; ++y)
  {
    for(int x=0; x<width; ++x)
    {
      if(fabs(a[x + y*width] - b[x + y*width]) > 1e-5)
      {
        printf("pixel x:%d, y:%d (%f, %f)\n", x, y, a[x + y*width], b[x + y*width]);
        return false;
      }
    }
  }
  return true;
}



double* create_example()
{
  double* ex = new double[9];

  ex[0] = 105;
  ex[1] = 102;
  ex[2] = 100;

  ex[3] = 103;
  ex[4] = 99;
  ex[5] = 103;

  ex[6] = 101;
  ex[7] = 98;
  ex[8] = 104;

  return ex;
}

uint8_t* zero_pad(uint8_t* mat, int width, int height, int padding)
{
  int new_width = width+padding*2, new_height = height+(padding*2);
  cout << "allocating : " << new_width * new_height << endl;
  uint8_t* ex = (uint8_t*)malloc(sizeof(uint8_t) * new_width*new_height);

  for(int i=0; i<new_width; ++i)
  {
    ex[i] = 0;
  }

  for(int i=1; i<height+1; ++i)
  {
    ex[i*(new_width)] = 0;
    memcpy(&ex[i*(new_width)+1], &mat[(i-1)*width], sizeof(uint8_t) * width);
    ex[i*(new_width)+width+1] = 0;
  }

  for(int i=0; i<new_width; ++i)
  {
    ex[(height+1)*(new_width)+i] = 0;
  }

  return ex;
}

int main(int argc, char** argv)
{
  int width, height;
  #ifdef USE_CIMG
  CImg<double> img_org(argv[1]);
  double* img = RGBSpaceToYCrCm(img_org);
  width = img_org->width();
  height = img_org->height();
  #else
  uint8_t *img = loadPgm(argv[1], &width, &height);
  #endif

  if(img == NULL)
  {
    printf("Image can't be loaded\n");
    exit(1);
  }

  printf("Image resolution : %dx%d\n", width, height);

  //Filter filter = createSharpeningFilter();
  Filter filter = createEdgeDetectionFilter();
  //Filter filter = createBlurFilter();

  DualConvol dual;
  /*NaiveConvol naive;
  UnravelConvol unravel;
  TripleConvol triple;
  LinearConvol linear;*/

  //double* naive_out = measure_convol(&naive, &img, filter);
  //double* unravel_out = measure_convol(&unravel, &img, filter);
  uint8_t* dual_out = measure_convol(&dual, img, filter, width, height);
  //double* triple_out = measure_convol(&triple, &img, filter);
  //double* linear_out = measure_convol(&linear, img, filter, width, height);

  //compareImgs(linear_out, dual_out, width, height);

#ifdef WRITE_DOWN
  //write_down_img(naive_out, argv[1], "output_naive.bmp");
  write_down_img(dual_out, "dual_output.pgm", width, height);
  /*write_down_img(triple_out, argv[1], "output_triple.bmp");
  write_down_img(linear_out, argv[1], "output_linear.bmp");
  write_down_img(unravel_out, argv[1], "output_unravel.bmp");*/
#endif

  delete[] filter->matrix;
  //delete[] img;
  delete filter;
  //delete naive_out;
  //delete unravel_out;
  //delete dual_out;
  //delete triple_out;
  //delete linear_out;
  free(img);
}

