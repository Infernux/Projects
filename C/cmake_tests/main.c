#include <stdio.h>
#include <stdlib.h>

#include "version.h"

#include "math_library/my_math.h"

int main()
{
  printf("Woot %d.%d\n", majVersion, minVersion);

  uint32_t val = 3;
  printf("Square of %d is %d\n", 3, u32_square(val));

  return 0;
}
