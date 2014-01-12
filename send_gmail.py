#!/usr/bin/python
import os, sys, getopt, smtplib, getpass
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders



def Send_email(subject, body, attach_dir, username, password):
   message = MIMEMultipart()
   message['From']    = username 
   message['To']      = username #this is the same as from
   message['Subject'] = subject #passed in from cmdline argument

   message.attach(MIMEText(body))
   part = MIMEBase('application', 'octet-stream')

   #you have to read the contents of the attachment so it can be encoded
   part.set_payload(open(attach_dir, 'rb').read())
   Encoders.encode_base64(part)
   part.add_header('Content-Disposition', 'attachment; filename="%s"'
                   %os.path.basename(attach_dir))
   message.attach(part) #actually adds the attachment to the email

   server = smtplib.SMTP('smtp.gmail.com:587')
   server.starttls()
   server.login(username, password)
   server.sendmail(username, username, message.as_string())
   server.quit()
   print "done"




def main(argv):
   # -s -> subject
   # -b -> body
   # -a -> attachment
   # -h -> help statement

   #defined these so in case user don't enter one it doesn't error
   subject = ''
   body = ''
   attach_dir = ''

   username = raw_input("Enter Email Address: ")
   #getpass.getpass() prompts the user for a password and doesn't display
   #what they type
   password = getpass.getpass()
   
   try:
      opts, args = getopt.getopt(argv, "hs:b:a:", [])
   except getopt.GetoptError:
      sys.exit()
   
   #gets the commandline arguments and passes values to variables
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -s <subject> -b <body> -a <attachment directory>'
         print 'Use quotes if you want to do multiple words for a field'
         sys.exit()
      elif opt in ('-s'):
         subject = arg
      elif opt in ('-b'):
         body = arg
      elif opt in ('-a'):
         attach_dir = arg

   print "subject is: ", subject
   print "body is: ", body
   print "attach dir is: ", attach_dir

   Send_email(subject, body, attach_dir, username, password)


if __name__ == '__main__':
   #passes it the cmdline args after the 1st one, since that's the filename
   main(sys.argv[1:])
