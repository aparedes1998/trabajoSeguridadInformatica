from threading import Thread
from Connection import Connection
import MailUtil
import UserController
import random
import string
from Database import saveUserFile, createFileEntry

MAX_ATTEMPTS = 3



class ClientThread(Thread):
    def __init__(self, address, socket):
        Thread.__init__(self)
        self.address = address
        # comprobar si la ip esta banneada
        self.connection = Connection(socket)
        print('New client connected from: ', address)

    def run(self):
        self.menuLogin()

    def menuLogin(self):
        while(True):
            self.connection.resetSecreto()         
            request = self.connection.receive()
            operacion = request['operacion']
            if operacion == 'Login':
                self.connection.send({
                    "operacion": "Login",
                    "resultado": "OK"
                })
                user = self.login()
                if user is None:
                    continue
                self.menu(user)
            elif operacion == "Register":
                self.connection.send({
                    "operacion": "Register",
                    "resultado": "OK"
                })
                self.register()
            elif operacion == "Recover":
                self.connection.send({
                    "operacion": "Recover",
                    "resultado": "OK"
                })
                self.recover()
            elif operacion == 'Exit':
                print(str(self.address) + " se ha desconectado")
                break

    def login(self):
        loggedIn = False
        for attempt in range(MAX_ATTEMPTS):
            self.connection.resetSecreto() 
            loginData = self.receiveLogin()            
            result = UserController.login(
                loginData['username'],
                loginData['password'])

            self.connection.secreto = eval(loginData['secret'])
            if result:              

                self.connection.send({
                    "Connection": "OK"
                })
                
                loggedIn = True
                return loginData['username']
                # guardar clave secreta
            elif attempt < MAX_ATTEMPTS-1:                
                self.connection.send({
                    "Connection": "ERROR"
                })
        if not loggedIn:
            # este seria un error distinto
            # bannear ip
            print(self.address, 'banned')
            self.connection.send({
                    "Connection": "BAN"
                })
            return None

    def register(self):
        registerData = self.receiveRegister()       
        result = UserController.register(
            registerData['username'],
            registerData['email'],
            registerData['password'])

        if result:
            self.connection.send({
                "operacion": "Register",
                "resultado": "OK"
            })
            public_key = self.connection.receive()
            bytes_as_bytes = eval(public_key['dataPubKey'])            
            UserController.savePublicKey(public_key['pubKeyName'], bytes_as_bytes)

            self.connection.send({
                "operacion": "Pub_key",
                "resultado": "OK"
            })

            # guardar clave secreta

        else:
            self.connection.send({
                "operacion": "Register",
                "resultado": "ERROR"
            })

    def recover(self):
        userName = self.receiveUsername()
        result = UserController.getEmail(userName)
        if result:
            codigo = ''.join(random.choice(
                string.ascii_uppercase + string.digits) for _ in range(8))
            MailUtil.sendRecovery(result, codigo)
            self.connection.send({
                "operacion": "RecoveryCode",
                "resultado": "OK"
            })
            cod = self.connection.receive()
            if (cod == codigo):
                self.connection.send({
                    "operacion": "ChangePassword",
                    "resultado": "OK"
                })
                newPassword = self.connection.receiveLogin()
                UserController.setNewPassword(userName, newPassword)
                self.connection.send("Contraseña cambiada con éxito")
            else:
                self.connection.send({
                    "operacion": "ChangePassword",
                    "resultado": "ERROR"
                })
                # Hecho asi , hay una sola oportunidad para poner el codigo correctamente
        else:
            self.connection.send({
                "operacion": "RecoveryCode",
                "resultado": "ERROR"
            })

    def menu(self, user):
        # User tiene en memoria durante la duración de la sesión el nombre de usuario de la persona.
        while(True):
            request = self.connection.receive()
            operacion = request['operacion']
            if operacion == 'Upload':
                self.connection.send({
                    "operacion": "Upload",
                    "resultado": "OK"
                })
                self.upload(user)
            elif operacion == "Share":
                self.connection.send({
                    "operacion": "Share",
                    "resultado": "OK"
                })
                self.share(user)
            
            elif operacion == "Download":
                self.connection.send({
                    "operacion": "Download",
                    "resultado": "OK"
                })
                self.download(user)
            elif operacion == "DownloadFrom":
                self.connection.send({
                    "operacion": "DownloadFrom",
                    "resultado": "OK"
                })
                self.downloadFrom(user)
            elif operacion == "ChangePassword":
                self.connection.send({
                    "operacion": "ChangePassword",
                    "resultado": "OK"
                })
                self.changePassword(user)
            elif operacion == 'Exit':
                print(str(self.address) + " ha cerrado sesión")
                break

    def upload(self, username):
        fileData = self.receiveUpload()
        if (fileData['operacion'] == "Upload" and fileData['resultado'] == "OK"):
            bytes_as_bytes = eval(fileData['dataArchivo'])
            result = saveUserFile(
                fileData['nombreArchivo'], bytes_as_bytes, username)
            fileCreated = createFileEntry(fileData['nombreArchivo'], username)
            if result and fileCreated:
                # agregar entrada a tabla archivos (rutaarchivo, owner)
                self.connection.send({
                    "operacion": "Upload",
                    "resultado": "OK"
                })

            else:
                self.connection.send({
                    "operacion": "Upload",
                    "resultado": "ERROR"
                })
        else:
            return

    def share(self, username):       

        tercerosData = self.receiveShare()

        if not (UserController.verifyFileExistance(tercerosData['nombreArchivo'],username)):   
            self.connection.send({
                "operacion": "share",
                "resultado": "error"
            })
            return
        fileName = tercerosData['nombreArchivo'] 
        usuarios = tercerosData['usuarios'].split(",")
        usuariosExistentes = map(UserController.verifyExistance, usuarios)
        listUsuariosExistentes = list(usuariosExistentes)
        for i , u in enumerate(usuarios):
            if listUsuariosExistentes[i]:
                public_key = UserController.getPublicKey(u)
                self.connection.send({
                    "operacion": "envioUsuarios",
                    "usuario": u,
                    "publicKey": str(public_key)             
                })
                respuesta = self.receiveShare()
                if (respuesta['resultado'] == "OK" ):
                    claveEncriptada = respuesta['claveEncriptada']
                    # Username: El que esta logueado
                    # U : Al que le estoy dando permiso
                    # ClaveEncriptada : Clave pública del que le estoy dando permiso                    
                    print("Permiso agregado con éxito")

        self.connection.send({
            "operacion": "finEnvioUsuarios"
        })
    def download(self, username):
        response = self.connection.receive()
        listaFiles = UserController.verPropios(username)
        tercerosData = self.connection.send({
            "operacion": "download",
            "listaArchivos": listaFiles
        })
        respuesta = self.connection.receive()

        if respuesta['operation'] == "download" and respuesta['resultado'] != "end":
            data = UserController.obtenerArchivoPropio(respuesta['filePath'])

            self.connection.send({
                "operacion": "download",
                "dataArchivo": str(data)                
            })

    def downloadFrom(self, username):
        response = self.connection.receive()
        listaFiles = UserController.verCompartidos(username)
        tercerosData = self.connection.send({
            "operacion": "downloadFrom",
            "listaArchivos": listaFiles
        })
        respuesta = self.connection.receive()

        if respuesta['operation'] == "downloadFrom" and respuesta['resultado'] != "end":
            data, key = UserController.obtenerArchivoDeTercero(respuesta['filePath'],username)

            self.connection.send({
                "operacion": "downloadFrom",
                "dataArchivo": str(data),
                "key": key
            })
        
    
    def changePassword(self, username):
        oldPassword = self.connection.receive()
        if (UserController.login(username, oldPassword['old'])):
            self.connection.send({
                "operacion":"ChangePassword",
                "resultado": "OK"
            })
            newPassword = self.connection.receive()
            UserController.setNewPassword(username, newPassword['pw'])
            self.connection.send({
                "operacion": "ChangePassword",
                "resultado" : "OK"
            })
        else:
            self.connection.send({
                "operacion":"ChangePassword",
                "resultado": "ERROR"
            })
        

    def receiveLogin(self):
        return self.connection.receiveLogin()

    def receiveRegister(self):
        return self.connection.receiveLogin()

    def receiveUsername(self):
        return self.connection.receive()

    def receiveUpload(self):
        return self.connection.receive()

    def receiveShare(self):
        return self.connection.receive()
        


