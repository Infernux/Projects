#ifndef QUEUE_H__
#define QUEUE_H__

#include <inttypes.h>
#include <pthread.h>

#include <pulse/context.h>

#define QUEUE_SUCCESS 1
#define QUEUE_FAILED 0

typedef struct Transaction_ {
  pa_operation*(*func)(pa_context*, void *args, int *fd);
  void *args;
  int *socket_fd;
} Transaction;

typedef struct Queue_ {
  Transaction *transactions;
  Transaction *head;
  uint32_t size;
  uint32_t current_index; /* tracks head's current index */
  uint32_t capacity;

  pthread_mutex_t mutex;
} Queue;

Queue* createQueue();
void freeQueue(Queue *queue);
uint8_t isFull(Queue *queue);
uint8_t isEmpty(Queue *queue);
Transaction pop(Queue *queue);
int8_t push(Queue *queue, Transaction transaction);

#endif /* QUEUE_H__ */
