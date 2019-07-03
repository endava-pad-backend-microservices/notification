import smtplib
import logging
from Utils import Constants
from email.message import EmailMessage
from Service.ConfigurationService import ConfigurationService

class MailService:
    def __init__(self):
        try:
            configurations = ConfigurationService().GetConfig()
            if(configurations.get(Constants.NOTIFICATION) and configurations[Constants.NOTIFICATION][Constants.MAILCONFIG]):
                self.sender = configurations[Constants.NOTIFICATION][Constants.MAILCONFIG]["sender"]
                self.port = configurations[Constants.NOTIFICATION][Constants.MAILCONFIG]["port"]
                self.server = configurations[Constants.NOTIFICATION][Constants.MAILCONFIG]["server"]
                self.user = configurations[Constants.NOTIFICATION][Constants.MAILCONFIG]["user"]
                self.password = configurations[Constants.NOTIFICATION][Constants.MAILCONFIG]["password"]
        except Exception:
            logging.warning("Fail to get Configuration for sending mail")

    def sendMail(self,destination,subject,message):
        try:
            msg = EmailMessage()
            msg.set_content(message,subtype='html')
            msg["Subject"] = subject
            msg["From"] = self.sender
            msg["To"] = destination
            smtpObj = smtplib.SMTP(self.server, int(self.port))
            smtpObj.starttls()
            smtpObj.login(self.user,self.password)
            smtpObj.send_message(msg)
            smtpObj.quit()
        except smtplib.SMTPException:
            logging.warning("Fail to send mail!!")

