all: server client

server: server.c
	gcc -g -o server server.c

client: client.c
	gcc -g -o client client.c

server_valgrind: server
	valgrind ./server

client_valgrind: client 
	valgrind ./client
