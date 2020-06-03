#include "client_socket.h"

#include <arpa/inet.h>
#include <sys/select.h>
#include <stdio.h>

#include "pa_helpers.h"

void *clients_handler(void *args) {
  printf("Started %s\n", __func__);

  Client_handler_args *cha = (Client_handler_args*)args;
  Clients_struct *cs = cha->clients_struct;
  printf("Queue size %d\n", cha->queue->size);

  struct timeval timeout = { .tv_sec =  1,
                           .tv_usec = 0 };

  push(cha->queue, list_sinks_inputs);

  do {
    fd_set active_set = cs->read_fds[0];
    /* select should return 0 on timeout */
    if(select(FD_SETSIZE, &active_set, NULL, NULL, &timeout) >= 0) {
      for(int i=0; i<FD_SETSIZE; ++i) {
        if(FD_ISSET(i, &active_set)) {
          printf("Select triggered\n");
          push(cha->queue, list_sinks);
          FD_CLR(i, &active_set);
        }
      }
    }else{
      printf("Select timed out\n");
    }
  } while(1);
}
