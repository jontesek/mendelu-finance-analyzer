#!/usr/local/bin/python2.7

# Import smtplib for the actual sending function
import smtplib
import smtpd

# Import the email modules we'll need
from email.mime.text import MIMEText

email_from = 'apps.noreply@petrovsky.cz'
emails_to = ['jond@post.cz']

# Create a text/plain message
msg = MIMEText("Dobry den, funguje to doufam.\nhello \nhelloo")
msg['Subject'] = 'pozdrav'
msg['From'] = email_from
msg['To'] = ','.join(emails_to)

#smtpd.SMTPServer(('localhost', 1025), None)
# wedos: smtp-mail1.wedos.net

# Send the message via our own SMTP server, but don't include the envelope header.
server = smtplib.SMTP('smtp.upcmail.cz', 25)
server.set_debuglevel(True)
#server.starttls()
#server.login('apps.noreply@petrovsky.cz', 'rpL6afik!')
server.sendmail(email_from, emails_to, msg.as_string())
server.quit()



