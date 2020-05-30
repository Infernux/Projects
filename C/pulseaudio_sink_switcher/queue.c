#include "queue.h"

#include <stdlib.h>

#include <pulse/context.h>

Queue* createQueue(uint32_t size) {
  Queue *queue = malloc(sizeof(Queue));
  queue->head = &queue->func[0];
  queue->size = 0;
  queue->current_index = 0;
  //queue->capacity = size;
  queue->capacity = MAX_QUEUE_SIZE;
  return queue;
}

void freeQueue(Queue *queue) {
  free(queue);
}

uint8_t isFull(Queue *queue) {
  return (queue->size == queue->capacity);
}

uint8_t isEmpty(Queue *queue) {
  return (queue->size == 0);
}

pa_operation*(*pop(Queue *queue))(pa_context*) {
  pa_operation*(*func)(pa_context*) = *queue->head;
  queue->current_index++;
  queue->current_index %= queue->capacity;
  queue->head = &queue->func[queue->current_index];
  queue->size--;

  return func;
}

/*
 * Returns QUEUE_SUCCESS on success
 * Returns QUEUE_FAILED on failure
 * */
int8_t push(Queue *queue, pa_operation*(*func)(pa_context*)) {
  if(isFull(queue)) {
    return QUEUE_FAILED;
  }

  uint32_t index = (queue->current_index + queue->size) % queue->capacity;
  queue->func[index] = func;
  queue->size++;

  return QUEUE_SUCCESS;
}
