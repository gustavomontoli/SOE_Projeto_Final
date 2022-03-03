import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Conta de e-mail que enviará a mensagem (apenas g-mail)
fromEmail = 'gustavomont97@gmail.com'
fromEmailPassword = 'isagus10'

# Conta de e-mail que receberá a mensagem
toEmail = 'anamatos67@gmail.com'


# Cria função sendEmail que passa o argumento image
# que será a imagem da pessoa detectada anexada no e-mail
def sendEmail(image):
    # Cria o cabeçalho do e-mail (Raiz da mensagem multiparte)
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'Atualização de Segurança'
    msgRoot['From'] = fromEmail
    msgRoot['To'] = toEmail
    msgRoot.preamble = 'Atualização da Câmera de Segurança Raspberry Pi'

    # Anexar a mensagem de texto
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)
    msgText = MIMEText('Câmera detectou uma pessoa')
    msgAlternative.attach(msgText)

    msgText = MIMEText('<img src="cid:image1">', 'html')
    msgAlternative.attach(msgText)

    # Abrir a imagem contida no diretório
    fp = open('Raspberry_Pi_4_Model_B_-_Side.jpg', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Anexar a imagem
    msgImage = MIMEImage(image)
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)

    # Conectar ao servidor
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(fromEmail, fromEmailPassword)
    smtp.sendmail(fromEmail, toEmail, msgRoot.as_string())
    smtp.quit()
