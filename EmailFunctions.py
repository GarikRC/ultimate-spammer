import smtplib
from email.mime.text import MIMEText
import time

__author__ = 'Qubasa'

def EmailSpammer(server, port, username, password, targetemail, fromemail, subject, msg, quantity):


    body = MIMEText(msg, 'plain')
    body['Subject'] = subject
    body['From'] = fromemail

    server = smtplib.SMTP(server, port)
    server.starttls()
    server.login(username, password)

    for i in range(quantity):
        server.sendmail(fromemail, targetemail, body.as_string())
        time.sleep(0.5)

    server.close()
