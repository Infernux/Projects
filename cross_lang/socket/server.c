#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/select.h>
#include <stdint.h>
#include <sys/socket.h>

#include "constants.h"

void dumpBuffer(char* buf, int len);
void myread(int client_fd, fd_set* read_fds);
void myread2(int client_fd, fd_set* read_fds);

int setupSocketUntilConnection()
{
  int server_fd, val;
  struct sockaddr_in add;
  int opt = 1;
  int addrlen = sizeof(add); //why ?

  if((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0)
  {
    perror("socket creation failed");
    return 1;
  }

  if(setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT,
                &opt, sizeof(opt)))
  {
    perror("failed setting socket options");
    return 1;
  }

  add.sin_family = AF_INET;
  add.sin_addr.s_addr = INADDR_ANY; //do not filter incoming address
  add.sin_port = htons(PORT);

  if(bind(server_fd, (struct sockaddr *)&add, sizeof(add)) < 0)
  {
    perror("bind failed");
    return 1;
  }

  printf("Waiting for a connection\n");

  if(listen(server_fd, MAX_INCOMING_CONNECTIONS) < 0)
  {
    perror("listen failed");
    return 1;
  }

  printf("Someone tried to connect, accept\n");
  return accept(server_fd, (struct sockaddr*)&add,
      (socklen_t*)&addrlen);
}

void testcast()
{
  char buff[30];
  int i;
  for(i=0; i<30; ++i)
  {
    buff[i] = 0;
  }
  buff[3] = 1;
  buff[4] = 'c';

  struct test_struct* a = (struct test_struct*)buff;
  printf("%d\n", a->a);
  printf("%c\n", a->str[0]);
}

int main()
{
  int client_fd;

  if((client_fd = setupSocketUntilConnection()) < 0)
  {
    perror("failed to create client socket");
    return 1;
  }

  printf("Accepted connection\n");

  struct timeval timeout = { .tv_sec =  1,
                           .tv_usec = 0 };
  fd_set read_fds;
  FD_ZERO(&read_fds);
  FD_SET(client_fd, &read_fds);

  do
  {
    //256 is garbage, use something else
    if(select(256, &read_fds, NULL, NULL, NULL) >= 0)
    {
      printf("Select triggered\n");
      if(FD_ISSET(client_fd, &read_fds))
      {
        myread2(client_fd, &read_fds);
      }else{
        printf("newt\n");
      }
    }else{
      printf("Select timed out\n");
    }
  }
  while(1);

  return 0;
}

void myread2(int client_fd, fd_set* read_fds)
{
  char lenbuff[4];
  int len;
  len = read(client_fd, lenbuff, sizeof(int));
  if(len == 0)
  {
    FD_CLR(client_fd, read_fds);
    printf("Disconnect\n");
    return;
  }

  while(len!=0){
    int* mylen = (int*)lenbuff;
    char* buff = malloc(sizeof(char)**lenbuff);
    len = read(client_fd, buff, *lenbuff);
    int i;
    for(i=0; i<*lenbuff; ++i)
    {
      printf("%c", buff[i]);
    }
    printf("\n");
    free(buff);
    len = read(client_fd, lenbuff, sizeof(int));
  }
}

void myread(int client_fd, fd_set* read_fds)
{
  char buff[30];
  int len;
  len = read(client_fd, buff, 30);
  if(len == 0)
  {
    FD_CLR(client_fd, read_fds);
    printf("Disconnect\n");
    return;
  }
  printf("struct:%d\n", sizeof(struct test_struct));
  struct test_struct* a = (struct test_struct*)buff;
  int i;
  printf("len:%d\n", a->a);
  for(i=0; i<a->a; ++i)
  {
    printf("%c", a->str[i]);
  }
  a=(struct test_struct*)&a->str[i];
  printf("len:%d\n", a->a);
  for(i=0; i<a->a; ++i)
  {
    printf("%c", a->str[i]);
  }
  printf("\n");
}

void dumpBuffer(char* buf, int len)
{
  printf("---- dump ----\n");
  int i;
  for(i=0; i<len; ++i)
  {
    printf("%d\n", buf[i]);
  }
  printf("---- end dump ----\n");
}
