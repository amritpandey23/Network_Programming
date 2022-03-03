# Write a Python Program to implement to Concurrent Server, Multiprotocol Server, Internet
# Super Server, Chat Server and Mail Server.

# Mail Server
# author: Amrit Pandey
# date: 03-03-2022

import smtplib
from email.mime.text import MIMEText

# sender information
sender = "amrit.pandey@gmail.com"
# receiver information
receivers = ["blog.admin@here.com"]

port = 1025
# text message
message = MIMEText('Hello email server!')

message['subject'] = 'a test email'
message['from'] = 'amrit.pandey@gmail.com'
message['to'] = 'blog.admin@here.com'

with smtplib.SMTP('localhost', port) as server:
    server.sendmail(sender, receivers, message.as_string())
    print('message was sent!')

