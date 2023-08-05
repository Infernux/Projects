#include "decorator.h"

#include <unistd.h>
#include <stdio.h>

#include <execinfo.h>
#include <string.h>

__attribute__((no_instrument_function))
static void print_function_name(char *fun_info)
{
  size_t info_len = strlen(fun_info);

  size_t i=0;
  size_t start = 0, end = 0, plus = 0;
  for(i=0; i<info_len; ++i)
  {
    if(fun_info[i] == '(')
    {
      start = i+1;
    }

    if(fun_info[i] == '+')
    {
      plus = i;
    }

    if(fun_info[i] == ')')
    {
      end = i;
      break;
    }
  }

  fun_info[plus] = '\0';
  fun_info[end] = '\0';

  if(plus == start)
  {
    printf("(call to static function %s)\n", &fun_info[plus+1]);
  } else {
    printf("(call to %s)\n", &fun_info[start]);
  }
}

__attribute__((no_instrument_function))
void __cyg_profile_func_enter(void *this_fn,
    void *call_fn)
{
  printf("own pid : %d\n", getpid());
  //char **sym = backtrace_symbols(&this_fn, 1);
  char **sym = backtrace_symbols(&this_fn, 1);
  print_function_name(sym[0]);
}
