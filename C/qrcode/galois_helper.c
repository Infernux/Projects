#include "galois_helper.h"

#include <stdio.h>

uint8_t gf256[256];
uint8_t gf256_antilog[256];

/*
 * in the galois field the following are true : 
 *  * (n == -n)
 *  * 
 * */

static void computeGF256(uint16_t modulo) {
  printf("--- %s ---\n", __func__);
  gf256[0] = 1; /* 2^0 */

  uint16_t prev = gf256[0];
  for(uint32_t i=1; i<256; ++i) {
    uint16_t current = prev * 2;
    if(current >= 256) {
      current ^= modulo;
    }
    prev = current;
    gf256[i] = current;
  }

  for(uint32_t i=0; i<256; ++i) {
    printf("%d : %d\n", i, gf256[i]);
  }
}

static void computeAntilogTable() {
  printf("--- %s ---\n", __func__);
  for(uint32_t alpha=1; alpha<256; ++alpha) {
    for(uint32_t antialpha=0; antialpha<256; ++antialpha) {
      if(gf256[antialpha] == alpha) {
        gf256_antilog[alpha] = antialpha;
        break;
      }
    }
  }

  for(uint32_t i=0; i<256; ++i) {
    printf("%d : %d\n", i, gf256_antilog[i]);
  }
}

void initialize_gf256(uint16_t modulo) {
  computeGF256(modulo);
  computeAntilogTable();
}
