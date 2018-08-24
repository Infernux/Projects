#ifndef COMMON__H_
#define COMMON__H_

#define CLIP(n) n > 255. ? 255. : n < 0. ? 0. : n

typedef struct s_Filter
{
  double* matrix;
  unsigned int width;
  unsigned int height;
} *Filter;

#endif
