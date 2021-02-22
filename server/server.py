from socket import socket
from ClientThread import ClientThread

HOST = ''
PORT = 9991

server = socket()
server.bind((HOST, PORT))

print("Server started")
print("Waiting for clients...")

while True:
    server.listen()
    clientSocket, clientAddress = server.accept()
    ClientThread(clientAddress, clientSocket).start()
