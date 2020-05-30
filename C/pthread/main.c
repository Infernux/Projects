#include <stdio.h>
#include <stdlib.h>

#include "pthread.h"

void *thread_run_function(void *args) {
  int *arg = (int*)args;
  printf("Passed value %d\n", *arg);
}

int main() {
  printf("Welcome to pthread\n");
  pthread_t thread;

  int parameter = 43;
  pthread_create(&thread, NULL, thread_run_function, &parameter);

  pthread_join(thread, NULL);
}
