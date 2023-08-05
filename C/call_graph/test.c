#include "test.h"

#include <stdio.h>

static void func1()
{
  printf("Hi, I'm func1\n");
}

void out_func1()
{
  printf("Hi, I'm out_func1\n");
  func1();
}
