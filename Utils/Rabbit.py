import logging
import threading

class AsyncRabbit:
    def __init__(self,connection,queue):
        logging.info("Creating: "+queue)
        self.connection = connection
        self.channel = connection.channel()
        self.queue = queue
    @classmethod
    def callback(self,ch, method, properties, body):
        logging.warning(body)

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