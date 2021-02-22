import Helpers
import Security


class Connection():
    def __init__(self, socket):
        self.socket = socket
        self.secreto = b'a'

    def encrypt(self, data):
        return Security.encrypt(data.encode('utf-8'), self.secreto)

    def decrypt(self, encryptedData):
        return Security.decrypt(encryptedData, self.secreto)

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

    def receiveLogin(self):
        encodedData = self.receiveData()        
        encryptedData = Helpers.decode(encodedData)
        jsonData = Security.decryptAsymPriv(eval(encryptedData), Security.getPrivKey())
        data = Helpers.fromJson(jsonData)
        return data

    def receiveData(self):
        size = self.receiveMessageSize()
        return self.socket.recv(size)

    def receiveMessageSize(self):
        size = self.socket.recv(4096)
        return int(size.decode('utf-8'))

    def resetSecreto(self):
        self.secreto = b'a'