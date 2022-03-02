import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage

# Conta de e-mail que enviará a mensagem (apenas g-mail)
fromEmail = 'email@gmail.com'
# Senha do e-mail (Para gerar uma senha: https://support.google.com/accounts/answer/185833?hl=en)
fromEmailPassword = 'password'

# Conta de e-mail que receberá a mensagem
toEmail = 'email2@gmail.com'

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
