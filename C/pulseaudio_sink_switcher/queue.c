#include "queue.h"

#include <stdlib.h>

Queue* createQueue(uint32_t size) {
  Queue *queue = malloc(sizeof(Queue));
  queue->head = queue;
  queue->size = 0; 
  queue->capacity = size;
  return queue;
}

void freeQueue(Queue *queue) {
  free(queue);
}

uint8_t isFull(Queue *queue) {
  return (queue->size == queue->capacity);
}
