#ifndef SOCKET_MANAGER_H__
#define SOCKET_MANAGER_H__

#include <arpa/inet.h>

#define PORT 25638
#define MAX_INCOMING_CONNECTIONS 3

/* not great */
typedef struct clients_struct_ {
  pthread_t clients[5];
  int fds[5];
  fd_set read_fds[5];
  uint32_t count;
} Clients_struct;

void* start_socket_manager(void *args);

#endif /* SOCKET_MANAGER_H__ */
