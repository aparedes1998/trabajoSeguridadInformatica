from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
import os
import os.path
from os import listdir
from os.path import isfile, join


__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))


class Security:
    def __init__(self):
        # Realizando el padding, se puede usar cualquier key que se te ocurra
        # Siempre y cuando no exceda el tamaño máximo de 32 bytes
        self.key = os.urandom(32)


def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)


def encrypt(message, key, key_size=256):
    key = pad(key)
    message = pad(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)


def encrypt_file(key, file_name):
    with open(file_name, 'rb') as f:
        plaintext = f.read()
    return encrypt(plaintext, key)


def decrypt(ciphertext, key):
    key = pad(key)
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")


def decrypt_file(key, file_name, ciphertext):
    plaintext = decrypt(ciphertext, key)
    with open(os.path.join(__location__, 'downloads/' + file_name), 'wb') as f:
        f.write(plaintext)


def generate_keys(username):
    private_key = rsa.generate_private_key(
        public_exponent=565467,
        key_size=2048,
        backend=default_backend()
    )

    public_key = private_key.public_key()
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(os.path.join(__location__, 'priv_' + username + '.pem'), "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    return pem


def getPrivKey(username):
    with open(os.path.join(__location__, 'priv_' + username + '.pem'), 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(), password=None, backend=default_backend()
        )
        return private_key


def getPubKey(pubKey):
    return serialization.load_pem_public_key(pubKey, backend=default_backend())


def getServerPubKey():
    with open(os.path.join(__location__, 'servpub.pem'), 'rb') as f:
        pub_key = serialization.load_pem_public_key(
            f.read(), backend=default_backend())
        return pub_key


def encryptAsymPub(data, public_key):
    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


def decryptAsymPriv(ciphertext, private_key):
    return private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
