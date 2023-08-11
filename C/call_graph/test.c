#include "test.h"

#include <stdio.h>

static void static_func1()
{
  printf("Hi, I'm func1\n");
}

static void static_func2()
{
  printf("Hi, I'm func2\n");
}

void out_func1()
{
  printf("Hi, I'm out_func1\n");
  static_func1();
  static_func2();
}
