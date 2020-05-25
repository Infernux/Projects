#include <inttypes.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#define MANTISSE 15
#define FIXED_POINT (32 - 1 - MANTISSE)

double fixed_to_double(const int32_t number)
{
  return number / (double)(1 << FIXED_POINT);
}

int32_t double_to_fixed(const double number)
{
  return round(number * (1 << FIXED_POINT));
}

int32_t fixed_mul(const int32_t number, const int32_t number2) {
  return ((int64_t)number * (int64_t)number2) >> FIXED_POINT;
}

int32_t fixed_div(const int32_t number, const int32_t number2) {
  return (((int64_t)number * (1 << FIXED_POINT)) / number2);
}

int main()
{
  double a = 5.234;
  double b = 3.234;

  printf("%f*%f -> %f, fixed %f\n",
      a,b,
      a*b,
      fixed_to_double(fixed_mul(double_to_fixed(a), double_to_fixed(b))));
  printf("%f/%f -> %f, fixed %f\n",
      a,b,
      a/b,
      fixed_to_double(fixed_div(double_to_fixed(a), double_to_fixed(b))));
}
