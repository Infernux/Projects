#include "socket_manager.h"

#include <stdio.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>

#include "client_socket.h"
#include "pa_helpers.h"
#include "pa_tlv_mapper.h"
#include "queue.h"
#include "tlv.h"

#define MAXSIZE 100

Clients_struct clients_struct;
uint8_t running = 1;

int32_t read_tlvs(int fd, Queue *queue, char *buffer, int32_t char_read) {
  TLV tlv;

  int processed = 0;
  char tmp[MAXSIZE];
  while(char_read > 0) {
    if(char_read < (int32_t)sizeof(int) * 2) {
      size_t needed = (int32_t)sizeof(int) * 2 - char_read;
      char_read = read(fd, &(buffer)[char_read], needed);
      char_read = (int32_t)sizeof(int) * 2;
      processed = 0;
    }

    int type = *(int*)&buffer[processed];
    int len  = *(int*)&buffer[processed + sizeof(int)];

    char_read -= sizeof(int) * 2;
    if(char_read < len) {
      size_t needed = len - char_read;
      printf("Reading more : %d (%d/%d)\n", needed, char_read, len);
      /* ewww */
      memcpy(tmp, &buffer[processed + sizeof(int) * 2 + char_read], char_read * sizeof(char));
      /* ewww */
      char_read += read(fd, &buffer[sizeof(int) * 2 + char_read], needed);
      processed = 0;
    }

    memcpy(tmp, &buffer[processed + sizeof(int) * 2], sizeof(char) * len);
    printf("Client sent type %d len %d : %s\n", type, len, tmp);

    tlv.type = type;
    tlv.length = len;
    tlv.value = tmp;

    add_tlv_value_to_queue(queue, &tlv);

    char_read -= sizeof(char) * len;
    processed += sizeof(char) * len + sizeof(int) * 2;
    printf("Remaining chars to process %d (processed %d)\n", char_read, processed);
  }
}

void* start_socket_manager(void *args) {
  printf("Started %s\n", __func__);

  Queue *queue = (Queue*)args;
  printf("Queue size %d\n", queue->size);

  memset(&clients_struct, 0, sizeof(Clients_struct));

  int server_fd, max_fd, val;
  struct sockaddr_in add;
  int opt = 1;
  int addrlen = sizeof(struct sockaddr_in);

  if((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0)
  {
    perror("socket creation failed");
    //pthread_join(client_manager, NULL);
    return NULL;
  }

  if(setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT,
                &opt, sizeof(opt)))
  {
    perror("failed setting socket options");
    //pthread_join(client_manager, NULL);
    return NULL;
  }

  add.sin_family = AF_INET;
  add.sin_addr.s_addr = INADDR_ANY; //do not filter incoming address
  add.sin_port = htons(PORT);

  if(bind(server_fd, (struct sockaddr *)&add, sizeof(struct sockaddr)) < 0)
  {
    perror("bind failed");
    //pthread_join(client_manager, NULL);
    return NULL;
  }

  printf("Waiting for a connection\n");
  if(listen(server_fd, 1) < 0)
  {
    perror("listen failed");
    //pthread_join(client_manager, NULL);
    return NULL;
  }

  FD_ZERO(&clients_struct.read_fds[0]);
  max_fd = server_fd;
  struct timeval timeout = { .tv_sec =  1,
                           .tv_usec = 0 };

  FD_SET(server_fd, &clients_struct.read_fds[0]);
  fd_set active_set;

  while(running) {
    active_set = clients_struct.read_fds[0];

    printf("Clients count %d\n", clients_struct.count);

    int select_res = select(FD_SETSIZE, &active_set, NULL, NULL, NULL);
    if(select_res == 0) {
      continue;
    }
    if(select_res < 0) {
      printf("Something really wrong happened\n");
      break;
    }
    for(int i=0; i<FD_SETSIZE && select_res > 0; ++i) {
      if(FD_ISSET(i, &active_set)) {
        select_res--;
        if(i == server_fd) {
          int newfd = accept(server_fd, (struct sockaddr*)&add,
              (socklen_t*)&addrlen);
          if(newfd < 0) {
            printf("Failure\n");
          }
          printf("-------\n");
          printf("Server fd %d\n", server_fd);
          printf("New connection (%d)\n", newfd);

          clients_struct.fds[clients_struct.count] = newfd;
          FD_SET(newfd, &clients_struct.read_fds[0]);
          if(newfd > max_fd) {
            max_fd = newfd;
          }
          clients_struct.count++; /* create a proper list of clients */
        } else {
          char buffer[MAXSIZE];
          int32_t char_read = read(i, buffer, MAXSIZE);
          if(char_read < 0) {
            printf("Read error (%d)\n", i);
            FD_CLR(i, &clients_struct.read_fds[0]);
            close(i);
          } else if (char_read == 0) {
            printf("EOF : client disconnected (%d)\n", i);
            printf("-------\n");
            FD_CLR(i, &clients_struct.read_fds[0]);
            clients_struct.count--;
          } else {
            /*
             * first consume what we read
             * if there is not more than 16 bytes, it means we can't have type and len
             * */
            read_tlvs(i, queue, buffer, char_read);

            while((char_read = read(i, buffer, MAXSIZE)) > 0) {
              read_tlvs(i, queue, buffer, char_read);
            }
            break;
          }
        }
      }
    }
  }

  //pthread_join(client_manager, NULL);
}
