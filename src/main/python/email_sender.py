import smtplib
import logging

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import getpass
 
#The mail addresses and password
sender_address = 'kumarshred2@gmail.com'
sender_pass = 'KubernetesCK@D123'

receiver_address = ['shreyas.dange22@gmail.com','akanksha.singh2908@gmail.com', 'dangesanand@gmail.com']

# #Setup the Logger
# logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
# rootLogger = logging.getLogger()

# fileHandler = logging.FileHandler("app.log")
# consoleHandler = logging.StreamHandler()

# fileHandler.setFormatter(logFormatter)
# consoleHandler.setFormatter(logFormatter)

# #Add Console and File Handlers both to Root Logger
# rootLogger.addHandler(consoleHandler)
# rootLogger.addHandler(fileHandler)
# rootLogger.setLevel(logging.INFO)

class EmailSender:
   
    @staticmethod
    def sendEmail(body):
        global receiver_address
        global sender_address
        global sender_pass
         
        if( body is not None):
            for address  in receiver_address:
                
                message = MIMEMultipart()
                message['From'] = sender_address
                message['To'] = address
                message['Subject'] = 'Vaccine Availability Alert.'   #The subject line

                #The body and the attachments for the mail
                message.attach(MIMEText(body, 'plain'))

                #Create SMTP session for sending the mail
                session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
                session.starttls() #enable security

                session.login(sender_address, sender_pass) #login with mail_id and password

                text = message.as_string()
                logging.info('Sending To : '+address)
                session.sendmail(sender_address,address, text)
                
                session.quit()
                logging.info('Mail Sent')