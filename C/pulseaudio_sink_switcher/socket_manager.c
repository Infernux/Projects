#include "socket_manager.h"

#include <stdio.h>

#include "pa_helpers.h"
#include "queue.h"

void* start_socket_manager(void *args) {
  printf("Started %s\n", __func__);

  Queue *queue = (Queue*)args;
  printf("Queue size %d\n", queue->size);

  sleep(3);
  push(queue, list_sinks_inputs);
  sleep(3);
  push(queue, list_sinks);
}
