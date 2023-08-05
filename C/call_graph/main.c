#include <stdio.h>

#include "test.h"

// needs to be compiled with -finstrument-functions
// and linked with -rdynamic

//extern char __etext;

static void static_function_to_call()
{
  printf("Woot2\n");
}

void function_to_call1()
{
  printf("Woot\n");
}

int main()
{
  printf("Welcome to main\n");

  function_to_call1();
  static_function_to_call();

  out_func1();

  //sleep(60);

  return 0;
}
