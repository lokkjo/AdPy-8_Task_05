
import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailProcessing:
    def __init__(self, address, password, smtp, imap):
        self.address = address
        self.password = password
        self.smtp = smtp
        self.imap = imap

    def send_message(self, recipients: list, subject: str,
                     message: str, header=None):
        self.subject = subject
        self.recipients = recipients
        self.message = message
        self.header = header

        # build message
        self.msg = MIMEMultipart()
        self.msg['From'] = self.address
        self.msg['To'] = ', '.join(self.recipients)
        self.msg['Subject'] = self.subject
        self.msg.attach(MIMEText(self.message))

        # send message
        self.mail_send = smtplib.SMTP(self.smtp, 587)
        # identify ourselves to smtp gmail client
        self.mail_send.ehlo()
        # secure our email with tls encryption
        self.mail_send.starttls()
        # re-identify ourselves as an encrypted connection
        self.mail_send.ehlo()
        self.mail_send.login(self.address, self.password)
        self.mail_send.sendmail(self.address, self.mail_send,
                                self.msg.as_string())
        self.mail_send.quit()
        # send end

    def receive_mail(self):
        # receive
        self.mail = imaplib.IMAP4_SSL(self.imap)
        self.mail.login(self.address, self.password)
        self.mail.list()
        self.mail.select('inbox')

        if self.header:
            self.header_string = self.header
        else:
            self.header_string = 'ALL'
        self.criterion = f'(HEADER Subject {self.header_string})'

        self.result, self.data = self.mail.uid('search', None,
                                               self.criterion)
        assert self.data[0], 'There are no letters with current header'

        self.latest_email_uid = self.data[0].split()[-1]
        self.result, self.data = self.mail.uid('fetch',
                                               self.latest_email_uid,
                                               '(RFC822)')
        self.raw_email = self.data[0][1]
        self.email_message = email.message_from_string(self.raw_email)

        self.mail.logout()
        # end receive


if __name__ == '__main__':
    login_mail = EmailProcessing('login@gmail.com', 'qwerty',
                                 'smtp.gmail.com', 'imap.gmail.com')

    # building message
    subject_text = 'Subject'
    recipients = ['vasya@email.com', 'petya@email.com']
    message_text = 'Message'

    login_mail.send_message(recipients, subject_text, message_text)

    login_mail.receive_mail()
