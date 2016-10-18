import smtplib
from email.mime.text import MIMEText


class MyMailer(object):
    """
    Send emails to administrator.
    """
    EMAIL_FROM = 'apps.noreply@petrovsky.cz'
    ERROR_EMAILS_TO = ['jond@post.cz']

    @classmethod
    def send_email(cls, email_from, emails_to, subject, text):
        """Send email to selected addresses."""
        # Create a text/plain message
        msg = MIMEText(text)
        msg['Subject'] = subject
        msg['From'] = email_from
        msg['To'] = ','.join(emails_to)
        
        # Send message via a STMP server.
        server = smtplib.SMTP('smtp.upcmail.cz', 25)    # open connection
        #server.set_debuglevel(True)
        server.sendmail(email_from, emails_to, msg.as_string())  # send message
        server.quit()   # close connection


    @classmethod
    def send_error_email(cls, subject, text):
        cls.send_email(cls.EMAIL_FROM, cls.ERROR_EMAILS_TO, subject, text)
