from getpass import getpass


def getCredentials():
    username = ''
    while username == '':
        print('Insert username:')
        username = input()

    password = ''
    while password == '':
        print('Insert password:')
        password = getpass()

    return {
        'username': username,
        'password': password
    }
