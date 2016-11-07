#-*- coding: utf-8 -*-
# auto publish my blog and email to me

import os
import re
import time

import smtplib

# my local blog path
my_blog_path="/work/blog"

# my git repos 
git_repository="git@github.com:xxlv/okuer.git"

# jekyll's default branch
git_branch="gh-pages"

# email config here
sender=os.environ.get('sender')
sender_host=os.environ.get('sender_host')
sender_port=os.environ.get('sender_port')
sender_pass=os.environ.get('sender_mail_pass')
my_notify_email=os.environ.get('my_notify_email','lvxiang119@gmail.com')


def publish_my_blog():
    """
    look for publish-abled file and do publish
    
    """
    
    # check my blog path files
    for root,dirs,files in os.walk(my_blog_path):

        for file in files:

            # check file name is ends with !
            # should_publish=re.search(r"/(.*?)\.md/",file)
            should_publish=file[-4]=="!"
            if(should_publish):
                do_publish(os.path.join(root,file))
            else:
                print("Nothing happend")

    # print("your email is %s " % my_notify_email)
    return



def do_publish(file):
    """
    check file and mv to git repositry and  push it 
    
    """
    
    new_file=file
    new_file=re.sub(r'(!)','',new_file)

    file_name=os.path.basename(new_file)
    gb=git_branch
    
    # parse category from file
    category="2016"

    # git clone
    # cp file to git repos
    # rename file remove !
    # git push

    tmp='/tmp/okuer/_posts'

    clone_shell= """
    
    git clone %s %s
    
    """ %(git_repository,"/tmp/okuer")

    if (not os.path.isdir(tmp)):

        res=os.popen(clone_shell).read()
        print(res)
        
    shell= """
    cd %s &&
    mv %s %s &&
    cp %s . &&
    git add %s &&
    git commit -m "%s" &&
    git push origin %s

    """ %(tmp+"/"+category,file,new_file,new_file,file_name,"Add new article "+file_name,git_branch)

    res=os.popen(shell).read()

    content="%s \n  %s"%(shell,res) 
    email_to(my_notify_email,content)

    return




def email_to(email,content):
    """
    simple email tool 
    
    """
    # todo
    print("Send a email to %s"% email)
    FROM=sender
    TO=[my_notify_email]
    SUBJECT="Auto publish your blog notify! "
    HOST=sender_host
    PORT=sender_port
    TEXT=content
    PASS=sender_pass
    
    message = """\
From: %s
To: %s
Subject: %s

 %s""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
    
    try:
        server=smtplib.SMTP_SSL(HOST,PORT)
        server.login(FROM,PASS)
        server.sendmail(FROM,TO,message)
        server.quit()
       
    except Exception as e:
        print("Email error")

    return                     



if __name__=="__main__":

    publish_my_blog()
