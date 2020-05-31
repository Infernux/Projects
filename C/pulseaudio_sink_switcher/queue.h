#ifndef QUEUE_H__
#define QUEUE_H__

#include <inttypes.h>
#include <pthread.h>

#include <pulse/context.h>

#define QUEUE_SUCCESS 1
#define QUEUE_FAILED 0

typedef struct Queue_ {
  pa_operation*(**func)(pa_context*);
  pa_operation*(**head)(pa_context*);
  uint32_t size;
  uint32_t current_index; /* tracks head's current index */
  uint32_t capacity;

  pthread_mutex_t mutex;
} Queue;

Queue* createQueue();
void freeQueue(Queue *queue);
uint8_t isFull(Queue *queue);
uint8_t isEmpty(Queue *queue);
pa_operation*(*pop(Queue *queue))(pa_context*);
int8_t push(Queue *queue, pa_operation*(*func)(pa_context*));

#endif /* QUEUE_H__ */
