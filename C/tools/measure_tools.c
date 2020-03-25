#include "measure_tools.h"

#ifdef TIME_MEASURE
#ifdef __unix__

#include <stdio.h>

#if defined(__android__)
#include <android/log.h>
#endif

void print_timediff(char *text, struct timespec *start, struct timespec *end)
{
  int s = end->tv_sec - start->tv_sec;
  long ns = end->tv_nsec - start->tv_nsec;
  if(ns < 0)
  {
    ns += 1e9;
    s--;
  }

  #if defined(__android__)
  __android_log_print(ANDROID_LOG_DEBUG, "Camera", "%s :\tTotal %5ds %3dms %3dus\n", text, s, (int)(ns / 1e6), (int)(ns / 1e3) % (int)1e3);
  #else
  printf("%s :\tTotal %5ds %3dms %3dus\n", text, s, (int)(ns / 1e6), (int)(ns / 1e3) % (int)1e3);
  #endif
}

#endif /* __unix__ */
#endif /* TIME_MEASURE */
