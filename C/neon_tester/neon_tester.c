#include <stdlib.h>
#include <stdio.h>

#ifdef __ARM_NEON
#include "arm_neon.h"

#include "bit_debug.h"

/* Adds 2 numbers, then divides the result by 2 */
void vhadd_test() {
  printf("---- %s ----\n", __func__);
  uint8x8_t a = {1,2,3,4,5,6,7,8};
  uint8x8_t b = {32,28,10,1,18,68,72,80};
  print_uint8x8_t("op1", a);
  print_uint8x8_t("op2", b);
  print_uint8x8_t("vqadd", vhadd_u8(a, b));
}

void add_test() {
  printf("---- %s ----\n", __func__);
  uint8x8_t a = {1,2,3,4,5,6,7,8};
  print_uint8x8_t("", a);
  print_uint8x8_t("+", a);
  print_uint8x8_t("=", vadd_u8(a, a));
}

/*
 * Add saturate : if the result overflows, the result is clamped to the max value
 * that can be held in an element
 * */
void vqadd_test() {
  printf("---- %s ----\n", __func__);
  uint8x8_t a = {128,2,3,4,5,6,7,8};
  uint8x8_t b = {200,28,10,1,18,68,72,80};
  print_uint8x8_t("op1", a);
  print_uint8x8_t("op2", b);
  print_uint8x8_t("vqadd", vqadd_u8(a, b));
}

/* only A64 */
#if 0
void vuqadd_test() {
  printf("---- %s ----\n", __func__);
  int8x8_t a = {127,2,3,-64,5,6,7,8};
  uint8x8_t b = {200,28,10,1,18,68,72,80};
  print_int8x8_t("op1", a);
  print_uint8x8_t("op2", b);
  print_int8x8_t("vuqadd", vuqadd_s8(a, b));
}
#endif

/*
 * Adds 2 vectors, then only returns the upper half
 * (in a half sized type (ie 16b -> 8b))
 * */
void vaddhn_test() {
  printf("---- %s ----\n", __func__);
  uint16x8_t a = {127,2,256,0,5,6,7,8};
  uint16x8_t b = {200,28,10,1,18,68,72,80};
  print_uint16x8_t("op1", a);
  print_uint16x8_t("op2", b);
  print_uint8x8_t("vaddhn", vaddhn_u16(a, b));
}

/* mad : op1 + (op2 * op3) */
void vmla_test() {
  printf("---- %s ----\n", __func__);
  uint8x8_t op1 = {127,  2,255,  0,  5,  6,  7,  8};
  uint8x8_t op2 = {  3, 28, 10,  1, 18, 68, 72, 80};
  uint8x8_t op3 = {  3, 28, 10,  1,  3, 68, 72, 80};
  print_uint8x8_t("",  op1);
  print_uint8x8_t("+", op2);
  print_uint8x8_t("*", op3);
  print_uint8x8_t("vmla", vmla_u8(op1, op2, op3));
}

/* msub : op1 - (op2 * op3) */
void vmls_test() {
  printf("---- %s ----\n", __func__);
  uint8x8_t op1 = {127,  2,255,  0,  5,  6,  7,  8};
  uint8x8_t op2 = {  3, 28, 10,  1, 18, 68, 72, 80};
  uint8x8_t op3 = {  3, 28, 10,  1,  3, 68, 72, 80};
  print_uint8x8_t("",  op1);
  print_uint8x8_t("-", op2);
  print_uint8x8_t("*", op3);
  print_uint8x8_t("vmls", vmls_u8(op1, op2, op3));
}

void main() {
  printf("Neon tester\n");

  //add_test();
  //vhadd_test();
  //vqadd_test();
  //vaddhn_test();
  //vmla_test();
  vmls_test();
}

#endif
