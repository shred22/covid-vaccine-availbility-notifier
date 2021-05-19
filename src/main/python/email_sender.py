import smtplib
import logging

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import getpass
import configparser
import os 
 
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../../../conf', 'config.ini'))

#The mail addresses and password
sender_address = config.get('mail', 'senderid')
sender_pass = config.get('mail', 'senderpassword')

receiver_address = []
receiverIds = config.get('mail', 'receiverids').split(',')
for receiverId in receiverIds:
    receiver_address.append(receiverId.strip())
print(receiver_address)

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