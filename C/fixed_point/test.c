#include <inttypes.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#define FIXED_POINT 27

double fixed_to_double(const int32_t number)
{
  return number / (double)(1 << FIXED_POINT);
}

int32_t double_to_fixed(const double number)
{
  return round(number * (1 << FIXED_POINT));
}

int main()
{
  printf("%f a\n", fixed_to_double((double_to_fixed(4.f) >> 16) * (double_to_fixed(2.f) >> 16)<<5));
}
