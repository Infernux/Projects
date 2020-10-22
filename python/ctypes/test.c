#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>

void printme() {
  printf("me !\n");
}

uint32_t doublenum(uint32_t x) {
  return x*2;
}

typedef struct mys_ {
  uint32_t x;
  uint32_t y;
}Mys;

uint32_t sum_val(Mys *val) {
  uint32_t acc = 0;
  for(int i=0; i < 5; ++i) {
    acc += val[i].x + val[i].y;
  }
  return acc;
}
