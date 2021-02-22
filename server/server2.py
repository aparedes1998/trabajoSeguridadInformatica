import socket
import os
import threading
import json
from base64 import b64encode, b64decode


class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket, name):
        threading.Thread.__init__(self)
        self.name = name
        self.csocket = clientsocket
        self.client = clientAddress
        print("New connection added: ", clientAddress)

    def run(self):
        print(clientAddress, "Waiting for log in")
        size = self.csocket.recv(4096)
        size = int(size.decode('utf-8'))

        bytesRead = self.csocket.recv(size)
        data = b64decode(bytesRead).decode('utf-8')
        #data = security.decrypt(encryptedData)
        data = json.loads(data)
        print(data)
        print(data['username'])
        result = '1' if data['password'] == '1234' else '0'
        response = b64encode(result.encode('utf-8'))
        bytesLength = len(response)
        print(bytesLength)
        self.csocket.sendall(bytes(str(bytesLength) + ' ', 'utf-8'))
        print(response)
        self.csocket.sendall(response)


LOCALHOST = ""
PORT = 9991
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")

i = 0
while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    i = i+1
    newthread = ClientThread(clientAddress, clientsock,
                             'Cliente'+str(i))
    newthread.start()
