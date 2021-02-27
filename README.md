# Obligatorio seguridad informática

El objetivo de este trabajo es crear una aplicación cliente-servidor por TCP donde las comunicaciones se encuentran encriptadas de punto a punto utilizando algoritmos de cifrado simétricos. Asimismo, el servicio que ofrece el servidor es el de la suba de archivos de forma segura, donde los mismos, se envían con la seguridad previamente descrita y además son almacenados con algoritmos simétricos utilizando una clave proveída por el usuario. 

## Funcionalidades

* Login utilizando un handshake para encriptar las comunicaciones

Una vez validado a un usuario a través de su email y contraseña, la aplicación creará una sesión encriptada punto a punto para mantener el resto de las comunicaciones.

* Registro de usuarios con contraseña e email. 

La contraseña se almacena hasheada en el servidor.

* Servicio de recuperación de clave utilizando el email.

El servidor posee un módulo con SMTP donde, al configurarsele un email emisor, será capaz de enviar códigos aleatorios de recuperación para comprobar la identidad de un usuario. Si el usuario intentando recuperar su cuenta ingresa el código correctamente, se le dará la opción de crear una nueva contraseña.

* Servicio de subida/descarga de archivos.

Como se explicó en el resumen del principio, el usuario podrá subir archivos al servidor. El usuario antes de envíar el archivo al servidor, designará una contraseña con la cual encriptar el archivo.

* Servicio de compartición de archivos.

Si un usuario lo desea, podrá dar acceso de sus archivos a otros usuarios, para ello, deberá proveer el nombre del usuario con el que se desea compartir el archivo y la clave de desencriptado del mismo. Esta clave será enviada al servidor encriptada con la clave pública del usuario al que se le desea compartir y se almacenará en el servidor. De esta manera, la clave será compartida de forma segura y el servidor no tendrá forma de ver dicha clave.

## Instalación

1 - Se necesitarán las siguientes librerías para el correcto funcionamiento de este programa:

* pycryptodome (o pycrypto en versiones viejas de python)
* cryptography
* hashlib

2 - Ir por consola hasta la carpeta "server" y ejecutar el siguiente comando:

```
python server.py
```

3 - Una vez teniendo el servidor corriendo, abrimos otra consola, nos paramos en la carpeta "client" y ejecutamos el siguiente comando:

```
python client.py
```

## Notas adicionales:

* El servidor es multihilo, por lo que se pueden tener de 1 a más clientes simultáneamente conectados.

* Tanto el cliente como el servidor pueden ser ejecutados en cualquier computadora, esto quiere decir que se puede correr el servidor en una computadora y el cliente en una o varias computadoras distintas y se conectarán a través de TCP.


