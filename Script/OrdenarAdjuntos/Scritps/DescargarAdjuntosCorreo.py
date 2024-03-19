## IMPORTACIONES DEL CÓDIGO.
import imaplib, re, email, requests
from email.header import decode_header
from email.utils import parsedate_tz, mktime_tz


## VARIABLES GENERALES DEL CÓDIGO.
email_user = 'carlos.vazquez@syscom.mx'
email_pass = 'sgcn mdbf rgro nsof'
imap_url = 'imap.gmail.com'
subject = 'Archivo de comprobantes'
from_email = 'notifications@mendel.com'
download_link = 'https://prod-somosmendel.s3-accelerate.amazonaws.com/...'
save_path = 'Adjuntos.zip'


## FUNCIONES GENERALES DEL CÓDIGO.
def ExtractDownloadLink(email_html):
    pattern = r'href="(https://prod-somosmendel\.s3-accelerate\.amazonaws\.com/[^\"]+)"'
    match = re.search(pattern, email_html, re.IGNORECASE)
    if match:
        return match.group(1)
    else:
        return None

def GenerateDownloadButtonLink(download_link, file_path='../Data/DescargarAdjuntos.html'):
    html_content = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Descargar Archivo</title>
        </head>
        <body>
            <div style="text-align: center; margin-top: 20%;">
                <a href="{download_link}" target="_blank" style="display: inline-block; background-color: #4CAF50; color: white; padding: 14px 25px; text-align: center; text-decoration: none; display: inline-block;">
                    Descargar Archivo
                </a>
            </div>
        </body>
        </html>
        '''
    with open(file_path, 'w') as file:
        file.write(html_content)

def GetNewestDownloadLink(subject, from_email, email_user, email_pass, imap_url):
    mail = imaplib.IMAP4_SSL(imap_url)
    mail.login(email_user, email_pass)
    mail.select("inbox")

    status, search_data = mail.search(None, '(SUBJECT "{}" FROM "{}")'.format(subject, from_email))
    if status != 'OK':
        print("No se encontraron correos con ese asunto del remitente especificado")
        return

    emails = [(num, mail.fetch(num, '(RFC822)')[1][0][1]) for num in search_data[0].split()]
    latest_email = None
    latest_date = None

    for num, data in emails:
        msg = email.message_from_bytes(data)
        date_tuple = parsedate_tz(msg['Date'])
        if date_tuple:
            email_date = mktime_tz(date_tuple)
            if latest_email is None or email_date > latest_date:
                latest_email = (num, msg)
                latest_date = email_date

    if latest_email:
        num, msg = latest_email
        email_body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    email_body = part.get_payload(decode=True).decode()
                    break
        else:
            email_body = msg.get_payload(decode=True).decode()

        download_link = ExtractDownloadLink(email_body)
        if download_link:
            print("Enlace de descarga encontrado.")
            GenerateDownloadButtonLink(download_link)
            mail.store(num, '+FLAGS', '\\Deleted')
        else:
            print("No se encontró el enlace de descarga.")
    else:
        print("No se encontró el correo más reciente.")

    mail.expunge()
    mail.logout()
    print("Correo procesado y eliminado.")


## MAIN DEL CODE.
if __name__ == "__main__":
    GetNewestDownloadLink(subject, from_email, email_user, email_pass, imap_url)