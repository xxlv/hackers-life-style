#-*- coding: utf-8 -*-

import smtplib
import sys
import os
import traceback

from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE,formatdate
from email import encoders
from email.mime.base import MIMEBase
from email.utils import make_msgid

rec_email=os.environ.get('kindle_email')  # kindle reciver email
sender=os.environ.get('kindle_sender')
sender_host=os.environ.get('kindle_sender_host')
sender_port=os.environ.get('kindle_sender_port')
sender_pass=os.environ.get('kindle_sender_mail_pass')


def push_file_to_my_kindle(files):
    """
        give files then push them to my kindle

    """
    subject="Send to kindle"
    content="Auto send to kindle"
    send_email(sender,rec_email,subject,content,files)


def send_email(send_from,to,subject,content,files):

    msg=MIMEMultipart()
    msg['From']=send_from
    msg['To']=to
    msg['Date']=formatdate(localtime=True)
    msg['Subject']=subject
    msg['Message-Id']=make_msgid()
    
    msg.attach(MIMEText(content))

    for f in files or []:
        with open(f,'rb') as fil:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(fil.read())

            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(f)))
            msg.attach(part)


    try:
        print("%s Send a mail to %s " % (send_from,to))

        smtp=smtplib.SMTP_SSL(sender_host,sender_port)
        smtp.login(sender,sender_pass)
        smtp.sendmail(send_from,to,msg.as_string())
        smtp.close()
    except smtplib.SMTPException:

        traceback.print_exc()



if __name__=='__main__':
 
    files=sys.argv
    files=files[1:]
    push_file_to_my_kindle(files)
