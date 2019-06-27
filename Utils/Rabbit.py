import logging
import threading
from Utils import MailEvents
from Service.ConfigurationService import ConfigurationService

class AsyncRabbit:
    def __init__(self,connection,queue):
        logging.info("Creating: "+queue)
        self.connection = connection
        self.channel = connection.channel()
        self.queue = queue

    def callback(self,ch, method, properties, body):
        if self.queue == "user_created":
            t = threading.Thread(target=MailEvents.mail_userCreated(body))
            t.daemon = True
            t.start()
        if self.queue == "update_config":
            ConfigurationService().UpdateConfig()
            logging.warning("Configuration updated!")

    def run(self):
        try:
            logging.info("Iniating consume: "+self.queue)
            self.channel.basic_consume(self.queue,self.callback,True)
            self.channel.start_consuming()
        except:
            if self.channel.is_open:
                self.channel.stop_consuming()
                self.channel.close()
            else:
                if self.connection.is_open:
                    self.connection.close()
            logging.warning("Closing rabbit Channel")
            threading.current_thread()._delete()
            raise Exception()