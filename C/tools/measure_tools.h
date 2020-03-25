#ifndef MEASURE_TOOLS_H__
#define MEASURE_TOOLS_H__

#define TIME_MEASURE
#ifdef TIME_MEASURE
#ifdef __unix__

#include <time.h>

void print_timediff(char *text, struct timespec *start, struct timespec *end);

#define TIME_INIT \
  struct timespec time_start, time_end;
#define TIME_START \
  clock_gettime(CLOCK_MONOTONIC, &time_start);
#define TIME_END(name) \
  clock_gettime(CLOCK_MONOTONIC, &time_end); \
    print_timediff(name, &time_start, &time_end);
#define TIME_CLEAN

#elif defined(__WIN32)
#include "Windows.h"

#if 1
  #define TIME_INIT LARGE_INTEGER start, end; \
    double PCFreq; \
    QueryPerformanceFrequency(&start); \
    PCFreq = (double)(start.QuadPart)/1000.0;

  #define TIME_START QueryPerformanceCounter(&start);

  #define TIME_END(name) QueryPerformanceCounter(&end); \
    printf("%s : %lfms\n", name, (double)(end.QuadPart - start.QuadPart)/PCFreq);

  #define TIME_CLEAN fclose(f);

#else
  #define TIME_INIT(filepath) WORD start, end; \
    FILE* f = fopen(filepath, "w");
  #define TIME_START start = GetTickCount();
  #define TIME_END(name) end = GetTickCount(); \
    fprintf(f, "%s : %d\n", name, (end - start));
  #define TIME_CLEAN fclose(f);
#endif

#else /* OS */

#error "time measurement NOT SUPPORTED on this OS"

#endif /* OS */

#else

#define TIME_INIT
#define TIME_START
#define TIME_END(name)
#define TIME_CLEAN

#endif

#endif /* MEASURE_TOOLS_H__ */
