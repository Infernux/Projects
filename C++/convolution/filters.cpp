#include "filters.h"

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

Filter createBlurFilter()
{
  Filter f = new s_Filter;
  f->width = 3;
  f->height = 3;
  f->matrix = new double[9];

  f->matrix[0] = 1./9.;
  f->matrix[1] = 1./9.;
  f->matrix[2] = 1./9.;

  f->matrix[3] = 1./9.;
  f->matrix[4] = 1./9.;
  f->matrix[5] = 1./9.;

  f->matrix[6] = 1./9.;
  f->matrix[7] = 1./9.;
  f->matrix[8] = 1./9.;

  return f;
}
