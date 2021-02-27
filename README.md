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

