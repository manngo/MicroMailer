import dns.resolver
import email, mimetypes, smtplib
from library import dbug

dbugging = False

def sendMail(data):
	message = email.message.EmailMessage()

	message['Subject'] = data['subject']
	message['From'] = data['from-address']
	message['To'] = data['to-address']
	message.set_content(data['message'])

	if attachment := data['attachment']:
		mime_type = mimetypes.guess_type(attachment)[0].split('/')
		with open(attachment, 'rb') as filehandle:
			content = filehandle.read()
			message.add_attachment(content, maintype=mime_type[0], subtype=mime_type[1])

	toAddressParts = email.utils.parseaddr(data['to-address'])[1].split('@')
	mx = [(i.preference, i.exchange.to_text()) for i in dns.resolver.resolve(toAddressParts[1], 'mx')]
	mail_server = sorted(mx)[0]
	dbug(mail_server[1])
	with smtplib.SMTP(mail_server[1]) as smtp:
		smtp.send_message(message)

	#	Cc
	del message['To']
#	message['To'] = fromAddressValue
	message['Cc'] = data['from-address']
	fromAddressParts = email.utils.parseaddr(data['from-address'])[1].split('@')
	mx = [(i.preference, i.exchange.to_text()) for i in dns.resolver.resolve(fromAddressParts[1],'mx')]
	mail_server = sorted(mx)[0]
	with smtplib.SMTP(mail_server[1]) as smtp:
		smtp.send_message(message)

def checkMail(data):
	errors = []

	if not data['subject']:
		errors.append('Missing Subject')
	if not data['from-address']:
		errors.append('Missing From Address')
	if not data['to-address']:
		errors.append('Missing To Address')
	if not data['message']:
		errors.append('Missing Message')

	if dbugging: dbug(f'''
	From: {data['from-address']}
	To: {data['to-address']}
	Subject: {data['subject']}
	Message: {data['message']}

	Attachment: {data['attachment']}
	''')

	return errors