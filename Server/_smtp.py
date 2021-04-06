import smtplib
import json
import threading


class SendEmail(threading.Thread):
    def __init__(self, to, subject, message):
        threading.Thread.__init__(self)
        self.to = to
        self.subject = subject
        self.message = message

    def run(self):
        try:
            file = open(f"Data/email.conf", "r")
            configuration = json.loads(file.read())
        except json.decoder.JSONDecodeError:
            return 1
        else:
            file.close()
        login = configuration['login']
        password = configuration['password']
        address = configuration['address']
        port = configuration['port']

        with smtplib.SMTP(address, port) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(login, password)
            smtp.sendmail(login, self.to,
                          f'Subject: {self.subject}\n\n{self.message}')


def send_email(to, subject, message):
    thread = SendEmail(to, subject, message)
    thread.start()


