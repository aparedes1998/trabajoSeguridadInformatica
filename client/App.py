import re
from Connection import Connection
import UserController
import Menu
import re
import os
from getpass import getpass
import Security

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))


class App:
    def __init__(self, host, port):
        self.connection = Connection(host, port)
        if self.connection.isConnected:
            while(True):
                self.connection.resetSecreto()
                opcion = Menu.menuLogin()
                if opcion == 1:
                    self.connection.send({
                        'operacion': 'Login'
                    })
                    response = self.connection.receive()
                    if (response['operacion'] == 'Login'
                            and response['resultado'] == 'OK'):
                        logged = self.login()
                        if (logged):
                            self.menu()
                elif opcion == 2:
                    self.connection.send({
                        'operacion': 'Register'
                    })
                    response = self.connection.receive()
                    if (response['operacion'] == 'Register'
                            and response['resultado'] == 'OK'):
                        self.register()
                elif opcion == 3:
                    self.connection.send({
                        'operacion': 'Recover'
                    })
                    response = self.connection.receive()
                    if (response['operacion'] == 'Recover'
                            and response['resultado'] == 'OK'):
                        self.recoverPassword()

                elif opcion == 4:
                    print("Sesion terminada.")
                    self.connection.send({
                        'operacion': 'Exit'
                    })
                    # No es necesario hacer nada, el hilo muere.
                    self.connection.close()
                    break

    def login(self):
        # TODO limitar cantidad de intentos y banear ip
        while True:
            self.connection.resetSecreto()
            self.sendLoginData()
            response = self.receiveLogInResponse()
            if response['Connection'] == 'OK':
                return True
            elif response['Connection'] == 'BAN':
                print('Too many fails, try again in 5 mins')
                return False
            else:
                print('Wrong credentials, try again')

    def sendLoginData(self):
        data = self.getLoginData()
        self.connection.sendLogin(data)

    def getLoginData(self):
        data = UserController.getCredentials()
        self.connection.secreto = os.urandom(31)
        data['secret'] = str(self.connection.secreto)
        self.username = data['username']
        return data

    def receiveLogInResponse(self):
        return self.connection.receive()

    def register(self):
        data = {}
        data['username'] = input('Nombre de usuario:')
        # Control de email válido
        while(True):
            data['email'] = input('Email: ')
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            if re.search(regex, data['email']):
                break
            else:
                print('Formato de mail inválido')
                print('Vuelva a ingresar el email')
                # TODO Agregar método que envie verifiacion de mail porque si no sabemos si el mail le marcha, no podemos reestablecer despues.
        while True:
            while True:
                print(
                    'Largo min: 8, Debe contener al menos: 1 caracter especial, 1 letra mayuscula, 1 minuscula, y 1 numero.')
                pw = getpass('Password: ')
                if verificarPassword(pw):
                    break
                print('Ese password no es lo suficientemente seguro, pruebe de nuevo.')

            data['password'] = pw
            if data['password'] == getpass('Repita password:'):
                break
            else:
                print('Los password no coinciden.')
                print('Vuelva a ingresar el password')
        self.connection.sendLogin(data)
        response = self.connection.receive()
        if response['resultado'] == 'OK':
            pubKeyName = 'pubkey_'+data['username']+'.pem'
            pubKey = Security.generate_keys(data['username'])
            self.connection.send({
                'pubKeyName': pubKeyName,
                'dataPubKey': str(pubKey)
            })
        else:
            print("Ya existe un usuario con ese nombre")
            return
        response = self.connection.receive()
        if response['resultado'] == 'OK':
            print('Registro completado')
        else:
            print('Algo salio mal')

    def recoverPassword(self):
        userName = input(
            'Por favor, si has olvidado tu contraseña, escribe tu nombre de usuario a continuación: ')
        self.connection.send(userName)
        response = self.connection.receive()
        if (response['operacion'] == 'RecoveryCode' and response['resultado'] == 'ERROR'):
            print("El username introducido no existe")
            return
        elif (response['operacion'] == 'RecoveryCode' and response['resultado'] == 'OK'):
            code = input(
                'Te hemos enviado un código a tu email, por favor escribelo a continuacion: ')
            self.connection.send(code)
            response = self.connection.receive()
            if (response['operacion'] == 'ChangePassword' and response['resultado'] == 'ERROR'):
                print("El codigo es incorrecto")
                return
            elif (response['operacion'] == 'ChangePassword' and response['resultado'] == 'OK'):
                while True:
                    while True:
                        print(
                            'Largo min: 8, Debe contener al menos: 1 caracter especial, 1 letra mayuscula, 1 minuscula, y 1 numero.')
                        newPassword = getpass('Ingrese su nueva clave: ')
                        if verificarPassword(newPassword):
                            break
                        print(
                            'Ese password no es lo suficientemente seguro, pruebe de nuevo.')

                    if newPassword == input('Vuelva a escribir su nueva clave: '):
                        break
                    else:
                        print('Las contraseñas no coinciden')
                        print('Vuelva a ingresar su nueva contraseña')
                self.connection.sendLogin(newPassword)
                response = self.connection.receive()
                print(response)

    def menu(self):
        while(True):
            opcion = Menu.menu()
            if opcion == 1:
                self.connection.send({
                    'operacion': 'Upload'
                })
                response = self.connection.receive()
                if (response['operacion'] == 'Upload' and response['resultado'] == 'OK'):
                    self.upload()

            elif opcion == 2:
                self.connection.send({
                    'operacion': 'Share'
                })
                response = self.connection.receive()
                if (response['operacion'] == 'Share' and response['resultado'] == 'OK'):
                    self.share()
            elif opcion == 3:
                self.connection.send({
                    'operacion': 'Download'
                })
                response = self.connection.receive()
                if (response['operacion'] == 'Download' and response['resultado'] == 'OK'):
                    self.download()
            elif opcion == 4:
                self.connection.send({
                    'operacion': 'DownloadFrom'
                })
                response = self.connection.receive()
                if (response['operacion'] == 'DownloadFrom' and response['resultado'] == 'OK'):
                    self.downloadFrom()
            elif opcion == 5:
                self.connection.send({
                    'operacion': 'ChangePassword'
                })
                response = self.connection.receive()
                if (response['operacion'] == 'ChangePassword' and response['resultado'] == 'OK'):
                    self.changePassword()
            elif opcion == 6:
                print("Sesion terminada.")
                self.connection.send({
                    'operacion': 'Exit'
                })
                break

    def upload(self):
        fileDirectory = input(
            'Ingresa la dirección donde tienes el archivo a continuación: ')
        if (os.path.isfile(fileDirectory)):  # Verifico si realmente es un archivo
            fileSplit = fileDirectory.split("/")
            fileName = fileSplit[-1]

            clave = input('Ingrese la clave especifica para el archivo: ')
            # chequear que clave sea menor a X caracteres

            # with open(fileDirectory, 'rb') as f:
            #     bFileData = f.read()

            bEncryptedFileData = Security.encrypt_file(
                clave.encode('utf-8'), fileDirectory)

            self.connection.send({
                "nombreArchivo": str(fileName),
                "dataArchivo": str(bEncryptedFileData),
                "operacion": "Upload",
                "resultado": "OK"
            })
            response = self.connection.receive()
            if (response['operacion'] == 'Upload' and response['resultado'] == 'OK'):
                print("Archivo subido con éxito")
        else:
            self.connection.send({
                "nombreArchivo": "None",
                "dataArchivo": "None",
                "operacion": "Upload",
                "resultado": "ERROR"
            })
            print("El directorio introducido no existe o ha sido eliminado")

    def createUser(self):
        pass

    def getFile(self):
        pass

    def sendFile(self):
        # encriptas simetricamente el archivo con clave X
        pass

    def share(self):
        fileName = input('Ingrese el nombre del archivo: ')
        clave = input('Ingrese la clave del archivo: ')
        # verificar que la clave sea correcta

        usuarios = input(
            "Ingrese los nombres de usuario que quiere dar acceso separados por coma (ej: 'usuario1,usuario2'): ")
        if usuarios == "":
            print("No ingreso ningun usuario.")
            return
        self.connection.send({
            "nombreArchivo": fileName,
            "usuarios": usuarios
        })

        response = self.connection.receive()
        if response['operacion'] == 'share' and response['resultado'] == 'error':
            print('El archivo no existe')
            return

        while (response['operacion'] == 'envioUsuarios'):
            pubKey = eval(response['publicKey'])
            public_key = Security.getPubKey(pubKey)

            encrypted_key = Security.encryptAsymPub(
                clave.encode('utf-8'), public_key)

            self.connection.send({
                'resultado': 'OK',
                'claveEncriptada': str(encrypted_key)
            })
            response = self.connection.receive()
        print('Archivo compartido con exito\n')

    def downloadFrom(self):
        self.connection.send({
            'resultado': 'OK'
        })
        data = self.connection.receive()

        if data['listaArchivos'] == []:
            print('No hay archivos compartidos contigo')
            self.connection.send({
                'operation': 'downloadFrom',
                'resultado': 'end'
            })
            return

        i = 0
        for file in data['listaArchivos']:
            filePathData = file.split('/')
            owner = filePathData[1]
            name = filePathData[2]
            print(str(i) + ' - ' + name + ' compartido por: ' + owner + '\n')
            i = i+1

        fileIndex = int(input('Escriba el numero del archivo a descargar: '))

        self.connection.send({
            'operation': 'downloadFrom',
            'filePath': data['listaArchivos'][fileIndex],
            'resultado': 'OK'
        })

        response = self.connection.receive()

        fileData = response['dataArchivo']
        fileName = data['listaArchivos'][fileIndex].split('/')[-1]

        encrypted_key = eval(response['key'])
        priv_key = Security.getPrivKey(self.username)
        bClave = Security.decryptAsymPriv(encrypted_key, priv_key)
        bFile = eval(fileData)
        Security.decrypt_file(bClave, fileName, bFile)

    def download(self):
        self.connection.send({
            'resultado': 'OK'
        })
        data = self.connection.receive()

        if data['listaArchivos'] == []:
            print('No tiene archivos')
            self.connection.send({
                'operation': 'download',
                'resultado': 'end'
            })
            return

        i = 0
        for file in data['listaArchivos']:
            filePathData = file.split('/')
            name = filePathData[2]
            print(str(i) + ' - ' + name + '\n')
            i = i+1

        fileIndex = int(input('Escriba el numero del archivo a descargar: '))

        self.connection.send({
            'operation': 'download',
            'filePath': data['listaArchivos'][fileIndex],
            'resultado': 'OK'
        })

        response = self.connection.receive()

        bEncFileRaw = response['dataArchivo']
        fileName = data['listaArchivos'][fileIndex].split('/')[-1]

        bEncFile = eval(bEncFileRaw)

        bClave = input('Ingrese la clave del archivo: ').encode('utf-8')

        Security.decrypt_file(bClave, fileName, bEncFile)

    def changePassword(self):
        old = getpass('Ingrese su contraseña actual:')
        self.connection.send({
            'operacion': 'changePassword',
            'old': old
        })
        response = self.connection.receive()

        if response['resultado'] == 'ERROR':
            print('Contraseña incorrecta')
            return

        while True:
            print(
                'Largo min: 8, Debe contener al menos: 1 caracter especial, 1 letra mayuscula, 1 minuscula, y 1 numero.')
            newPW = getpass('Ingrese su contraseña nueva: ')
            if verificarPassword(newPW):
                break
            print('Ese password no es lo suficientemente seguro, pruebe de nuevo.')

        check = getpass('Repita su contraseña nueva:')

        while newPW != check:
            print('Las contraseñas no coinciden\n')
            print(
                'Largo min: 8, Debe contener al menos: 1 caracter especial, 1 letra mayuscula, 1 minuscula, y 1 numero.')
            newPW = getpass('Ingrese su contraseña nueva: ')
            if verificarPassword(newPW):
                break
            print('Ese password no es lo suficientemente seguro, pruebe de nuevo.')
            check = getpass('Repita su contraseña nueva:')

        self.connection.send({
            'operacion': 'changePassword',
            'pw': newPW
        })

        response = self.connection.receive()

        if response['resultado'] == 'OK':
            print('Contraseña cambiada con exito')
        else:
            print('Algo salio mal')


def verificarPassword(clave):
    TAMANO_MINIMO_CLAVE = 8
    CARACTERES_ESPECIALES = re.compile('[.@_!#$%^&*()<>?/\|}{~:]')

    if len(clave) < TAMANO_MINIMO_CLAVE:
        return False
    elif re.search('[0-9]', clave) is None:
        return False  # No contiene un número
    elif re.search('[A-Z]', clave) is None:
        return False  # No contiene al menos una mayúscula
    elif re.search('[a-z]', clave) is None:
        return False  # No contiene al menos una minúscula
    elif CARACTERES_ESPECIALES.search(clave) == None:
        return False
    else:
        return True
