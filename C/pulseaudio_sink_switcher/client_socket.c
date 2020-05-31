#include "client_socket.h"

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
    if(select(cs->count, cs->read_fds, NULL, NULL, &timeout) >= 0) {
      for(int i=0; i<cs->count; ++i) {
        if(FD_ISSET(cs->fds[i], cs->read_fds)) {
          printf("Select triggered\n");
          push(cha->queue, list_sinks);
        }
      }
    }else{
      printf("Select timed out\n");
    }
  } while(1);
}
