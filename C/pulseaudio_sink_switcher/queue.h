#ifndef QUEUE_H__
#define QUEUE_H__

#include <inttypes.h>

#include <pulse/context.h>

#define MAX_QUEUE_SIZE 5

typedef struct Queue_ {
  pa_operation*(*func[MAX_QUEUE_SIZE])(pa_context*);
  pa_operation*(*head)(pa_context*);
  uint32_t size;
  uint32_t capacity;
} Queue;

Queue* createQueue();
void freeQueue(Queue *queue);

#endif /* QUEUE_H__ */
