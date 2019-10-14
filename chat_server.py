#! /usr/bin/env python3
from socket import AF_INET,socket,SOCK_STREAM
from threading import Thread
clients = {}
addreses = {}

HOST = '127.0.0.1'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def accept_incoming():
	while True:
		client,client_address = SERVER.accept()
		print(f'connected to {client_address}')
		client.send(bytes('hey,type your name','utf8'))
		addreses[client] = client_address
		Thread(target = handle_client, args =(client,)).start()


def handle_client(client):
	name = client.recv(BUFSIZ).decode('utf8')
	client.send(bytes(f'welcome {name} if you want to exit type quit','utf8'))
	broadcast(bytes(f'{name} name has joined the chat' ,'utf8'))
	clients[client] = name
	while True:
		msg = client.recv(BUFSIZ)
		if msg != 'quit':
			broadcast(msg,name +': ')
		else:
			client.send(bytes('quit','utf8'))
			client.close()
			del clients[client]
			broadcast(bytes(f'{name} has left the chat','utf8'))
			break
def broadcast(msg,prefix = ''):
	for sock in clients:
		sock.send(bytes(prefix,'utf8')+msg)


if __name__ =='__main__':
	SERVER.listen(5)
	print('waiting for connection...')
	ACCEPT_THREAD = Thread(target = accept_incoming)
	ACCEPT_THREAD.start()
	ACCEPT_THREAD.join()
	SERVER.close()
