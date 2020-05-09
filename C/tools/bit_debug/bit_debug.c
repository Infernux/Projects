#include "bit_debug.h"

#include <stdio.h>

#ifdef __ARM_NEON
#include "arm_neon.h"
void print_uint8x8_t(const char *title, uint8x8_t v) {
  printf("%10s : ",title);
  uint8_t *u8_el = (uint8_t*)&v;
  for(uint32_t el=0; el<7; ++el) {
    PRINT_BYTE(u8_el[el]);
    printf(",");
  }
  PRINT_BYTE(u8_el[7]);
  printf("\n");
}

void print_uint8x16_t(const char *title, uint8x16_t v) {
  printf("%10s : ",title);
  uint8_t *u8_el = (uint8_t*)&v;
  for(uint32_t el=0; el<15; ++el) {
    PRINT_BYTE(u8_el[el]);
    printf(",");
  }
  PRINT_BYTE(u8_el[15]);
  printf("\n");
}

void print_uint16x4_t(const char *title, uint16x4_t v) {
  printf("%10s : ",title);
  uint16_t *u16_el = (uint16_t*)&v;
  uint32_t el=0;
  for(el=0; el<3; ++el) {
    PRINT_BYTE(u16_el[el] & 0xff00);
    printf(" ");
    PRINT_BYTE(u16_el[el] & 0xff);
    printf(",");
  }
  PRINT_BYTE(u16_el[el] & 0xff00);
  printf(" ");
  PRINT_BYTE(u16_el[el] & 0xff);
  printf("\n");
}

void print_uint16x8_t(const char *title, uint16x8_t v) {
  printf("%10s : ",title);
  uint16_t *u16_el = (uint16_t*)&v;
  uint32_t el=0;
  for(el=0; el<7; ++el) {
    PRINT_BYTE(u16_el[el] & 0xff00);
    printf(" ");
    PRINT_BYTE(u16_el[el] & 0xff);
    printf(",");
  }
  PRINT_BYTE(u16_el[el] & 0xff00);
  printf(" ");
  PRINT_BYTE(u16_el[el] & 0xff);
  printf("\n");
}
#endif
