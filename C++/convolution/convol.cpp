#include <stdio.h>
#include <iostream>
#include <string.h>

#include "unravel_convol.h"
#include "naive_convol.h"
#include "dual_convol.h"
#include "common.h"

#include "CImg.h"

#define Kr 0.299
#define Kg 0.587
#define Kb 0.114

using namespace cimg_library;
using namespace std;

void print_timediff(struct timespec *start, struct timespec *end)
{
  int s = end->tv_sec - start->tv_sec;
  int ns = end->tv_nsec - start->tv_nsec;
  cout << s * 1000 + ns / 1000000 << "ms" << endl;
}

void apply_filter(double* out, double* padded_img, Filter filter, int width, int height, int padding);
double naive_convol(double* img, Filter filter, int x, int y, int stride);
double* zero_pad(double* mat, int width, int height, int padding);

double* RGBSpaceToYCrCm(CImg<double> img)
{
  double* out = new double[img.width() * img.height()];

  for(int j=0; j<img.height(); ++j)
  {
    for(int i=0; i<img.width(); ++i)
    {
      double red = img(i, j, 0);
      double green = img(i, j, 1);
      double blue = img(i, j, 2);

      out[i+j*img.width()] = Kr*red + Kg*green + Kb*blue;
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

Filter createEdgeDetectionFilter()
{
  Filter f = new s_Filter;
  f->width = 3;
  f->height = 3;
  f->matrix = new double[9];
  f->matrix[0] = -1;
  f->matrix[1] = -1;
  f->matrix[2] = -1;

  f->matrix[3] = -1;
  f->matrix[4] = 8;
  f->matrix[5] = -1;

  f->matrix[6] = -1;
  f->matrix[7] = -1;
  f->matrix[8] = -1;

  return f;
}

Filter createSharpeningFilter()
{
  Filter f = new s_Filter;
  f->width = 3;
  f->height = 3;
  f->matrix = new double[9];

  f->matrix[0] = 0.;
  f->matrix[1] = -1.;
  f->matrix[2] = 0.;

  f->matrix[3] = -1.;
  f->matrix[4] = 5.;
  f->matrix[5] = -1.;

  f->matrix[6] = 0.;
  f->matrix[7] = -1.;
  f->matrix[8] = 0.;

  return f;
}

typedef void (*filter_applier)(double* out, double* padded_img, Filter filter, int width, int height, int padding);

void measure_convol(filter_applier fa, char* img_path, string output, Filter filter)
{
  CImg<double> img(img_path);
  printf("w: %d, h: %d\n", img.width(), img.height());

  double* img2 = RGBSpaceToYCrCm(img);

  int width = img.width(), height = img.height();
  int padding = 1;
  double* padded_img = zero_pad(img2,width,height,padding);

  struct timespec start, end;
  clock_gettime(CLOCK_MONOTONIC, &start);

  fa(img2, padded_img, filter, width, height, padding);

  clock_gettime(CLOCK_MONOTONIC, &end);
  print_timediff(&start, &end);

  YCrCmSpaceToRGB(&img, img2, 0, width, height);

  delete[] padded_img;
  delete img2;
  img.save(output.c_str());
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

double* zero_pad(double* mat, int width, int height, int padding)
{
  int new_width = width+padding*2, new_height = height+(padding*2);
  cout << "allocating : " << new_width * new_height << endl;
  double* ex = new double[new_width*new_height];

  for(int i=0; i<new_width; ++i)
  {
    ex[i] = 0;
  }

  for(int i=1; i<height+1; ++i)
  {
    ex[i*(new_width)] = 0;
    memcpy(&ex[i*(new_width)+1], &mat[(i-1)*width], sizeof(double) * width);
    ex[i*(new_width)+width+1] = 0;
  }

  for(int i=0; i<new_width; ++i)
  {
    ex[(height+1)*(new_width)+i] = 0;
  }

  return ex;
}

double* load_img(const char* path)
{
  CImg<double> src(path);
  return src;
}

int main(int argc, char** argv)
{
  //Filter filter = createSharpeningFilter();
  Filter filter = createEdgeDetectionFilter();

  measure_convol(apply_filter, argv[1], "output_naive.bmp", filter);
  measure_convol(apply_filter_unravel, argv[1], "output_unravel.bmp", filter);
  measure_convol(apply_filter_dual, argv[1], "output_dual.bmp", filter);

  delete[] filter->matrix;
  //delete[] img;
  delete filter;
}
