#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/select.h>
#include <stdint.h>
#include <sys/socket.h>

#include "constants.h"

int main()
{
  int client_socket;
  struct sockaddr_in add;

  if((client_socket = socket(AF_INET, SOCK_STREAM, 0)) == 0)
  {
    perror("socket creation failed");
    return 1;
  }

  add.sin_family = AF_INET;
  add.sin_port = htons(PORT);
  add.sin_addr.s_addr = htonl(INADDR_LOOPBACK);

  if(connect(client_socket, (struct sockaddr*)&add, sizeof(struct sockaddr_in)) != 0)
  {
    perror("socket connection failed");
    return 1;
  }

  fd_set write_fds;
  FD_ZERO(&write_fds);
  FD_SET(client_socket, &write_fds);

  struct test_struct buff = {.a = 4};
  buff.str = malloc(sizeof(char) * 4);
  buff.str[0] = 'a';
  buff.str[1] = 'a';
  buff.str[2] = 'a';
  buff.str[3] = 'b';

  if(select(256, NULL, &write_fds, NULL, NULL) >= 0)
  {
      if(FD_ISSET(client_socket, &write_fds))
      {
        write(client_socket, (void*)&buff, sizeof(int32_t));
        write(client_socket, (void*)buff.str, sizeof(char)*buff.a);
      }
  }

  free(buff.str);

  if(close(client_socket)!=0)
  {
    perror("");
    return 1;
  }
}
