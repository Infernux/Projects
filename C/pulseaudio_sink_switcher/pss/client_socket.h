#ifndef CLIENT_SOCKET_H__
#define CLIENT_SOCKET_H__

#include "queue.h"

#include "socket_manager.h"

typedef struct clients_handler_args_ {
  Clients_struct *clients_struct;
  Queue *queue;
} Client_handler_args;

void *clients_handler(void *args); /* args : Queue */

#endif /* CLIENT_SOCKET_H__ */
