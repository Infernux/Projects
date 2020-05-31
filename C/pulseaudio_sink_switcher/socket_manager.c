#include "socket_manager.h"

#include <stdio.h>
#include <string.h>
#include <arpa/inet.h>

#include "client_socket.h"
#include "queue.h"

Clients_struct clients_struct;

void* start_socket_manager(void *args) {
  printf("Started %s\n", __func__);

  Queue *queue = (Queue*)args;
  printf("Queue size %d\n", queue->size);

  memset(&clients_struct, 0, sizeof(Clients_struct));
  Client_handler_args cha;
  cha.clients_struct = &clients_struct;
  cha.queue = queue;

  pthread_t client_manager;
  pthread_create(&client_manager, NULL, clients_handler, &cha);

  int server_fd, val;
  struct sockaddr_in add;
  int opt = 1;
  int addrlen = sizeof(struct sockaddr_in);

  if((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0)
  {
    perror("socket creation failed");
    pthread_join(client_manager, NULL);
    return NULL;
  }

  if(setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT,
                &opt, sizeof(opt)))
  {
    perror("failed setting socket options");
    pthread_join(client_manager, NULL);
    return NULL;
  }

  add.sin_family = AF_INET;
  add.sin_addr.s_addr = INADDR_ANY; //do not filter incoming address
  add.sin_port = htons(PORT);

  if(bind(server_fd, (struct sockaddr *)&add, sizeof(struct sockaddr)) < 0)
  {
    perror("bind failed");
    pthread_join(client_manager, NULL);
    return NULL;
  }

  printf("Waiting for a connection\n");

  if(listen(server_fd, MAX_INCOMING_CONNECTIONS) < 0)
  {
    perror("listen failed");
    pthread_join(client_manager, NULL);
    return NULL;
  }

  printf("Someone tried to connect, accept\n");
  clients_struct.fds[clients_struct.count] = accept(server_fd, (struct sockaddr*)&add,
      (socklen_t*)&addrlen);
  printf("accepted\n");

  FD_ZERO(&clients_struct.read_fds[clients_struct.count]);
  FD_SET(clients_struct.fds[clients_struct.count], &clients_struct.read_fds[clients_struct.count]);
  clients_struct.count++;

  pthread_join(client_manager, NULL);
}
