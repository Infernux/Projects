#include <stdlib.h>
#include <stdio.h>

#ifdef __ARM_NEON
#include "arm_neon.h"

#include "bit_debug.h"

void main() {
  printf("Neon tester\n");

  uint8x8_t a = {1,2,3,4,5,6,7,8};
  print_uint8x8_t("a", a);
}

#endif
