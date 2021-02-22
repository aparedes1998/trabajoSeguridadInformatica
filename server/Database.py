import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))

SEPARATOR = "<SEPARATOR>"
def loadUser(username):
    with open(os.path.join(__location__, 'databases/users.csv'), 'r') as users:
        for user in users:
            user = user.replace("\n", "")
            userData = user.split(',')

            if userData[0] == username:

                return {
                    'passwordHash': userData[2],
                    'salt': userData[3]
                }
    return None


def getEmailfromUser(username):
    with open(os.path.join(__location__, 'databases/users.csv'), 'r') as users:
        for user in users:
            user = user.replace("\n", "")
            userData = user.split(',')
            if userData[0] == username:
                return userData[1]
    return None


def saveUser(username, email, password, salt):
    with open(os.path.join(__location__, 'databases/users.csv'), 'a') as users:
        users.write(str(username)+","+str(email)+"," +
                    str(password)+","+str(salt)+"\n")
        newpath = os.path.join(__location__, 'userData/'+username)
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        return True

    return False


def setNewPasswordForUser(username, newPassword,salt):
    linea = -1
    with open(os.path.join(__location__, 'databases/users.csv'), 'r') as users:
        for i, user in enumerate(users):
            user = user.replace("\n", "")
            userData = user.split(',')
            if userData[0] == username:
                linea = i
    if linea == -1:
        return False
    replace_line(linea, newPassword,salt)
    return True


def replace_line(line_num, newPassword,salt):
    with open(os.path.join(__location__, 'databases/users.csv'), 'r') as users:
        lines = users.readlines()
        userData = lines[line_num].replace("\n", "").split(',')
        userData[2] = newPassword
        userData[3] = salt
        newLine = userData[0]+","+userData[1] + \
            ","+userData[2]+","+userData[3]+"\n"
        lines[line_num] = newLine

    with open(os.path.join(__location__, 'databases/users.csv'), 'w') as out:
        out.writelines(lines)


def saveUserFile(fileName, fileData, userName):
    with open(os.path.join(__location__, 'userData/'+str(userName)+"/"+fileName), 'wb') as f:
        f.write(fileData)
        return True
    return False


def createFileEntry(fileName, username):
    with open(os.path.join(__location__, 'databases/files.csv'), 'a') as files:
        files.write("userData/" + str(username)+"/"+fileName+SEPARATOR+str(username)+"\n")
       
        return True
    return False


def lookupFile(fileName, username):
    return os.path.isfile(os.path.join(__location__, "userData/"+username+"/"+fileName))


def addPermission(userOwner, userShare, publicKeyShare, nomArchivo):
    with open(os.path.join(__location__, 'databases/permissions.csv'), 'a') as permissions:
        permissions.write("userData/"+userOwner+"/"+nomArchivo +SEPARATOR+ userShare + SEPARATOR+ publicKeyShare+"\n")
        return True
    return False

def buscarCompartidos(username):
    files = []
    with open(os.path.join(__location__, 'databases/permissions.csv'), 'r') as permissions:
        for user in permissions:
            user = user.replace("\n", "")
            userData = user.split(SEPARATOR)

            if userData[1] == username:
                files.append(userData[0])
        return files
    return None

def buscarPropios(username):
    filesUser = []
    with open(os.path.join(__location__, 'databases/files.csv'), 'r') as files:
        for f in files:
            user = f.replace("\n", "")
            userData = user.split(SEPARATOR)

            if userData[1] == username:
                filesUser.append(userData[0])
        return filesUser
    return None



def obtenerArchivoTercero(filePath):
    with open(os.path.join(__location__, filePath) , 'rb') as f:
        fileData = f.read()
        return fileData
    return None

def obtenerClaveArchivoTercero(filePath,username):
    with open(os.path.join(__location__, 'databases/permissions.csv'), 'r') as permissions:
        for user in permissions:
            user = user.replace("\n", "")
            userData = user.split(SEPARATOR)

            if userData[1] == username and userData[0] == filePath:
                return userData[2]
        return None
    return None
                
def guardarClavePublica(nombreArchivo, data):
    with open(os.path.join(__location__, 'public_keys/'+nombreArchivo), "wb") as f:
        f.write(data)
        return True
    return False

def obtenerPublicKey(username):
    with open(os.path.join(__location__, 'public_keys/'+"pubkey_"+username+".pem"), "rb") as f:        
        return f.read()
    return None

