import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sendRecovery(destinatario, codigo):
    mensaje = "Utiliza este código para recuperar tu contraseña: " + codigo
    sendMail(destinatario, mensaje, "Recuperacion de clave")


def sendMail(destinatario, mensaje, asunto):
    contenidoMensaje = mensaje
    # TMail y contraseña
    direccion_emisor = 'somemail@email.com'
    clave_emisor = 'YOUR_PASSWORD'
    direccion_destinatario = str(destinatario)
    # Hacemos un MIME para estructurar el mensaje
    mensaje = MIMEMultipart()
    mensaje['From'] = direccion_emisor
    mensaje['To'] = direccion_destinatario
    mensaje['Subject'] = asunto

    # Cuerpo y asunto del mensaje
    mensaje.attach(MIMEText(contenidoMensaje, 'plain'))

    # Creamos una sesion SMTP para enviar el mensaje
    # Cambiar acordemente al servidor de correo utilizado
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()  # Ponemos TLS en el mensaje para seguridad
    session.login(direccion_emisor, clave_emisor)  # Login
    text = mensaje.as_string()
    session.sendmail(direccion_emisor, direccion_destinatario, text)
    session.quit()
    print('Mail Sent')
