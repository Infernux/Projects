#include <stdio.h>
#include <iostream>
#include <string.h>

#include "CImg.h"

using namespace cimg_library;
using namespace std;

typedef struct s_Filter
{
  double* matrix;
  unsigned int width;
  unsigned int height;
} *Filter;

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

  f->matrix[0] = 0;
  f->matrix[1] = -1;
  f->matrix[2] = 0;

  f->matrix[3] = -1;
  f->matrix[4] = 5;
  f->matrix[5] = -1;

  f->matrix[6] = 0;
  f->matrix[7] = -1;
  f->matrix[8] = 0;

  return f;
}

double naive_convol(double* img, Filter filter, int x, int y)
{
  double n = 0.f;
  int stride = 5;
  for(int j=-1; j<2; ++j)
  {
    for(int i=-1; i<2; ++i)
    {
      n += img[x+i + (y+j)*stride] * filter->matrix[i+1 + (j+1)*filter->width];
    }
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

  int padding = 1, width = img.width(), height = img.height();
  double* padded_img = zero_pad(img,width,height,padding);

  for(int y=0 + padding; y<height + padding; ++y)
  {
    for(int x=0 + padding; x<width + padding; ++x)
    {
      naive_convol(padded_img, filter, x, y);
      img[(x-padding) + ((y-padding) * height)] = naive_convol(padded_img, filter, x, y);
    }
  }

  img.save("output.bmp");

  delete[] filter->matrix;
  delete[] padded_img;
  //delete[] img;
  delete filter;
}
