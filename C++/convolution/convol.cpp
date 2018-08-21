#include <stdio.h>
#include <iostream>
#include <string.h>

#include "CImg.h"

#define Kr 0.299
#define Kg 0.587
#define Kb 0.114

using namespace cimg_library;
using namespace std;

typedef struct s_Filter
{
  double* matrix;
  unsigned int width;
  unsigned int height;
} *Filter;

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

void apply_filter(double* out, Filter filter, int width, int height)
{
  int padding = 1;
  double* padded_img = zero_pad(out,width,height,padding);

  for(int y=0 + padding; y<height + padding; ++y)
  {
    for(int x=0 + padding; x<width + padding; ++x)
    {
      out[(x-padding) + (y-padding) * width] = naive_convol(padded_img, filter, x, y, (width+padding*2));
    }
  }

  delete[] padded_img;
}

double naive_convol(double* img, Filter filter, int x, int y, int stride)
{
  //flip kernel
  int n = 0.f;
  for(int j=-1; j<2; ++j)
  {
    for(int i=-1; i<2; ++i)
    {
      n += img[x+i + (y+j)*stride] * filter->matrix[i+1 + (j+1)*filter->width];
    }
  }
  if(n < 0.)
  {
    return 0.;
  }
  else if(n > 255.)
  {
    return 255.;
  }
  return n;
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
  Filter filter = createSharpeningFilter();
  //double* img = create_example();
  //double* img = load_img(argv[1]);
  CImg<double> img(argv[1]);
  printf("w: %d, h: %d\n", img.width(), img.height());

  double* img2 = RGBSpaceToYCrCm(img);

  int width = img.width(), height = img.height();
  apply_filter(img2, filter, width, height);

  YCrCmSpaceToRGB(&img, img2, 0, width, height);

  img.save("output.bmp");

  delete[] filter->matrix;
  //delete[] img;
  delete filter;
  delete img2;
}
