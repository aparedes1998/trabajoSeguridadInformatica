import json
from base64 import b64encode, b64decode


def encode(data):
    return b64encode(data.encode('utf-8'))


def utf8encode(text):
    return bytes(text, 'utf-8')


def decode(data):
    return b64decode(data).decode('utf-8')


def toJson(data):
    return json.dumps(data)


def fromJson(jsonData):
    return json.loads(jsonData)
