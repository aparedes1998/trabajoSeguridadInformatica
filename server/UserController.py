from Database import *
from Security import hash
import random
import string


def login(username, password):
    """ hashear username y buscarlo en base de datos
    si hay coincidencia, traer el hash del password y su salt string
    hashear password+salt y comparar con password
    luego almacenar clave secreta del usuario y responder OK"""
    #usernameHash = hash(username)
    user = loadUser(str(username))
    if not user:
        return False
    passwordHash = hash(password+user['salt'])    
    return str(passwordHash) == user['passwordHash']

def register(username, email, password):
    #Si el usuario existe
    if verifyExistance(username):
        return False
    #usernameHash = hash(username)   
    salt = ''.join(random.choice(
                string.ascii_uppercase + string.digits) for _ in range(8))
    passwordHash = hash(password+salt)
    return saveUser(username, email,  passwordHash, salt)    
    

## Devuelve si un usuario ya existe en la base de datos con ese nombre
def verifyExistance(username):
    #usernameHash = hash(username)
    user = loadUser(username)    
    if not user:        
        return False
    return True

def getEmail(username):
    if (verifyExistance(username)):
        usernameHash = username
        emailUser = getEmailfromUser(usernameHash)
        return emailUser
    return None

def setNewPassword(username, newPassword):
    salt = ''.join(random.choice(
                string.ascii_uppercase + string.digits) for _ in range(8)) ##Generar string randomico 
    return setNewPasswordForUser(username, hash(newPassword+salt),salt)

def verifyFileExistance(nomArchivo, username):
    return lookupFile(nomArchivo, username)

def saveAccess(userOwner, userShare, publicKeyShare, nomArchivo):
    return addPermission(userOwner, userShare, publicKeyShare, nomArchivo)

def verCompartidos(username):
    return buscarCompartidos(username)

def verPropios(username):
    return buscarPropios(username)

def obtenerArchivoDeTercero(filePath, username):
    archivo = obtenerArchivoTercero(filePath)
    publicKey = obtenerClaveArchivoTercero(filePath,username)
    return archivo, publicKey

def obtenerArchivoPropio(filePath):
    archivo = obtenerArchivoTercero(filePath)    
    return archivo

def savePublicKey(nombreArchivo, data):
    return guardarClavePublica(nombreArchivo,data)

def getPublicKey(username):
    return obtenerPublicKey(username)