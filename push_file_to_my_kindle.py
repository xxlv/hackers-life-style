#-*- coding: utf-8 -*-


import smtplib
import sys
import os

from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE,formatdate


rec_email=os.environ.get('kindle_email')
sender=os.environ.get('kindle_sender')
sender_host=os.environ.get('kindle_sender_host')
sender_port=os.environ.get('kindle_sender_port')
sender_pass=os.environ.get('kindle_sender_mail_pass')


def push_file_to_my_kindle(files):
    subject="Convert"
    content="Convert"
    send_email(sender,rec_email,subject,content,files)


def send_email(send_from,to,subject,content,files):
    msg=MIMEMultipart()
    msg['From']=send_from
    msg['To']=to
    msg['Date']=formatdate(localtime=True)
    msg['Subject']=subject

    msg.attach(MIMEText(content))
    for f in files or []:
        with open(f,'rb') as fil:
            part=MIMEApplication(fil.read(),Name=basename(f))
            part['Content-Disposition']='attachment;filename="%s"' % basename(f)
            msg.attach(part)

    print("%s Send a mail to %s " % (send_from,to))
    smtp=smtplib.SMTP_SSL(sender_host,sender_port)
    smtp.login(sender,sender_pass)
    smtp.sendmail(send_from,to,msg.as_string())
    smtp.close()



if __name__=='__main__':
    files=sys.argv
    files=files[1:]
    push_file_to_my_kindle(files)
