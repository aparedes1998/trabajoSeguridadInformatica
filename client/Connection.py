from socket import socket
from Security import encryptAsymPub, getServerPubKey, decrypt as decryptSym, encrypt as encryptSym
import Helpers


class Connection:
    def __init__(self, host, port):
        self.secreto = b'a'
        self.socket = socket()
        try:
            self.socket.connect((host, port))
            self.isConnected = True
        except ConnectionRefusedError:
            print('Couldn\'t connect')
            self.isConnected = False

    def close(self):
        self.socket.close()
        self.isConnected = False

    def encrypt(self, data):
        return encryptSym(data.encode('utf-8'), self.secreto)

    def decrypt(self, encryptedData):
        return decryptSym(encryptedData, self.secreto)

    def sendLogin(self, data):
        jsonData = Helpers.toJson(data)
        encryptedData = self.encryptLogin(jsonData)
        encodedData = Helpers.encode(str(encryptedData))
        self.sendData(encodedData)

    def encryptLogin(self, data):
        pubKey = getServerPubKey()
        bData = data.encode('utf-8')
        return encryptAsymPub(bData, pubKey)

    def send(self, data):
        jsonData = Helpers.toJson(data)
        encryptedData = self.encrypt(jsonData)
        encodedData = Helpers.encode(str(encryptedData))
        self.sendData(encodedData)

    def sendData(self, data):
        self.sendMessageSize(data)
        self.socket.sendall(data)

    def sendMessageSize(self, data):
        size = len(data)
        sizeEncoded = Helpers.utf8encode(str(size))
        self.socket.sendall(sizeEncoded)

    def receive(self):
        encodedData = self.receiveData()
        encryptedData = Helpers.decode(encodedData)
        jsonData = self.decrypt(eval(encryptedData))
        data = Helpers.fromJson(jsonData)
        return data

    def receiveData(self):
        size = self.receiveMessageSize()
        return self.socket.recv(size)

    def receiveMessageSize(self):
        size = self.socket.recv(4096)
        return int(size.decode())

    def resetSecreto(self):
        self.secreto = b'a'
