#include "queue.h"

#include <stdlib.h>
#include <stdio.h>

#include <pulse/context.h>

Queue* createQueue(uint32_t size) {
  Queue *queue = malloc(sizeof(Queue));
  queue->transactions = malloc(sizeof(Transaction) * size);
  queue->head = &queue->transactions[0];
  queue->size = 0;
  queue->current_index = 0;
  queue->capacity = size;
  pthread_mutex_init(&queue->mutex, NULL);
  return queue;
}

void freeQueue(Queue *queue) {
  free(queue->transactions);
  pthread_mutex_destroy(&queue->mutex);
  free(queue);
}

/* not thread safe ! */
uint8_t isFull(Queue *queue) {
  return (queue->size == queue->capacity);
}

uint8_t isEmpty(Queue *queue) {
  pthread_mutex_lock(&queue->mutex);
  uint8_t b_isEmpty = (queue->size == 0);
  pthread_mutex_unlock(&queue->mutex);
  printf("empty : %d\n", b_isEmpty);
  return (b_isEmpty);
}
/* not thread safe ! */

Transaction pop(Queue *queue) {
  pthread_mutex_lock(&queue->mutex);
  printf("%s, %p %p\n", __func__, queue->head->func,queue->head->args);
  Transaction transaction = *queue->head;
  queue->current_index++;
  queue->current_index %= queue->capacity;
  queue->head = &queue->transactions[queue->current_index];
  queue->size--;
  printf("size %d\n", queue->size);
  pthread_mutex_unlock(&queue->mutex);

  return transaction;
}

/*
 * Returns QUEUE_SUCCESS on success
 * Returns QUEUE_FAILED on failure
 * */
int8_t push(Queue *queue, Transaction transaction) {
  pthread_mutex_lock(&queue->mutex);
  if(isFull(queue)) {
    pthread_mutex_unlock(&queue->mutex);
    return QUEUE_FAILED;
  }

  printf("%s\n", __func__);

  uint32_t index = (queue->current_index + queue->size) % queue->capacity;
  queue->transactions[index] = transaction;
  queue->size++;
  pthread_mutex_unlock(&queue->mutex);

  return QUEUE_SUCCESS;
}
