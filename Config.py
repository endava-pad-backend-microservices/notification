import py_eureka_client.eureka_client as eureka_client
import configparser
from os import environ
from Service.ConfigurationService import ConfigurationService
from Utils import Constants
import pika
from Utils.Rabbit import AsyncRabbit
import logging
import threading
import time as time

def configure():
    config = configparser.ConfigParser()
    config.read("app.ini")

    ##App's port configuration
    if config.has_option("app",Constants.NOTIFICATION_PORT) == False:
        raise SystemError("Fail! Port is not configured.")
    if config.has_option("app",Constants.NOTIFICATION_URL) == False:
        raise SystemError("Fail! Port is not configured.")

    port = config["app"][Constants.NOTIFICATION_PORT]
    if environ.get(Constants.NOTIFICATION_PORT):
        port = environ.get(Constants.NOTIFICATION_PORT)
    host = config["app"][Constants.NOTIFICATION_URL]
    if environ.get(Constants.NOTIFICATION_URL):
        host = environ.get(Constants.NOTIFICATION_URL)

    try:
        connectEureka(config,port)
    except Exception:
        logging.warning("Eureka is down! Exiting...")
        raise SystemError()
    try:
        configurations = ConfigurationService().GetConfig()
    except Exception:
        logging.error("Continuing without Configurations")
        raise SystemError()
    try:
        if configurations != None:
            connectRabbit(config,configurations)
    except:
        logging.warning("Rabbit is not fully available. Exiting..")
        raise SystemError()
    configurations["host"] = host
    configurations["port"] = port
    return configurations

def connectEureka(config,port):
     ##Eureka configuration
    eureka_server = None
    if config.has_option("app",Constants.EUREKA_SERVER) != False:
        eureka_server = config["app"][Constants.EUREKA_SERVER]

    if environ.get(Constants.EUREKA_SERVER):
        eureka_server = environ.get(Constants.EUREKA_SERVER)

    if eureka_server == None:
        raise Exception("Eureka is not define!")
    else:
        try:
            eureka_client.init(eureka_server = eureka_server,app_name="Notification",instance_port=int(port))
        except:
            raise Exception("Fail to Connect to Eureka")

def connectRabbit(config,configurations):
    if configurations != None and configurations.get(Constants.NOTIFICATION) and configurations[Constants.NOTIFICATION]["queues"]:
        rabbitServer = None
        rabbitPort = None

        if config.has_option("app",Constants.RABBIT_SERVER) != False:
            rabbitServer = config["app"][Constants.RABBIT_SERVER]
            rabbitPort = config["app"][Constants.RABBIT_PORT]
            rabbitUser = config["app"][Constants.RABBIT_USER]
            rabbitPass = config["app"][Constants.RABBIT_PASS]
        if environ.get(Constants.RABBIT_SERVER):
            rabbitServer = environ.get(Constants.RABBIT_SERVER)
            rabbitPort = environ.get(Constants.RABBIT_PORT)
            rabbitUser = environ.get(Constants.RABBIT_USER)
            rabbitPass = environ.get(Constants.RABBIT_PASS)

        if rabbitServer != None and rabbitPort != None and rabbitUser != None and rabbitPass != None:
            logging.info("Connecting to: "+rabbitServer+":"+rabbitPort)
            rabbitList = list()
            try:
                credentials = pika.PlainCredentials(rabbitUser,rabbitPass)
                for queue in configurations[Constants.NOTIFICATION]["queues"]:
                    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitServer,port=rabbitPort,credentials=credentials))
                    r = AsyncRabbit(connection=connection,queue=queue)
                    thread = threading.Thread(name=queue,target=r.run)
                    thread.daemon = True
                    thread.start()
                    rabbitList.append(queue)
            except:
                if connection.is_open:
                    connection.close()
                logging.warning("Fail to connect to rabbit")
                raise Exception()
            time.sleep(1) ##porque sino no llega a controlar si hubo conexion
            threadList = [t.getName() for t in threading.enumerate()]
            for rQueue in rabbitList:
                if rQueue not in threadList:
                    logging.warning(rQueue+ " queues is not up! Failing..")
                    raise Exception()