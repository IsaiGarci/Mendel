import sys
import imaplib
import email
import os
import time

EMAIL_ACCOUNT = "bot1@syscom.mx"
EMAIL_FOLDER = "INBOX"

def process_mailbox(M):
    rv, data = M.search(None, '(SUBJECT "Archivo de transacciones")')
    if rv != 'OK' or not data[0]:
        print("No se encontraron mensajes!")
        return False

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print("ERROR obteniendo mensajes", num)
            return False
        
        msg = email.message_from_bytes(data[0][1])
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True).decode('utf-8')
                    break
        else:
            body = msg.get_payload(decode=True).decode('utf-8')
        
        print('Almacenando correo:', num)
        with open(os.path.join(r'C:\ProduccionRpa\Mendel\Correo', f'index.html'), 'w', encoding='utf-8') as file:
            file.write(body)

        # Marcar el mensaje para eliminación
        M.store(num, '+FLAGS', '\\Deleted')

    # Guardar un indicador cuando se procesan todos los correos
    with open(os.path.join(r'C:\ProduccionRpa\Mendel\Correo', f'listo.txt'), 'w', encoding='utf-8') as file:
        file.write('Si')

    # Llamar EXPUNGE para eliminar permanentemente todos los mensajes marcados
    M.expunge()
    return True

M = imaplib.IMAP4_SSL('imap.gmail.com')
try:
    rv, data = M.login(EMAIL_ACCOUNT, '&C97&K*w8Buc')
except imaplib.IMAP4.error as e:
    print(f"Error el iniciar sesión!!! {EMAIL_ACCOUNT} - {e}")
    sys.exit(1)

print(rv, data)

rv, mailboxes = M.list()
if rv == 'OK':
    print("Bandeja: INBOX")

while True:
    rv, data = M.select(EMAIL_FOLDER)
    if rv == 'OK':
        print("Procesando bandeja: INBOX...\n")
        found = process_mailbox(M)
        if found:
            break
        time.sleep(60)  # Espera 60 segundos antes de revisar nuevamente
    else:
        print("ERROR: Imposible abrir bandeja ", rv)

M.close()
M.logout()
