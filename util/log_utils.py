import os
import logging


def setup_logs():
    if not os.path.exists("./orgdata"):
        os.makedirs("./orgdata")
    if os.path.exists("./orgdata/landing_zone.log"):
        os.remove("./orgdata/landing_zone.log")
    logging.basicConfig(format='%(levelname)s|%(asctime)s|%(message)s', filename='./orgdata/landing_zone.log', level=logging.INFO)


def formatmessage(filename, classname, methodname, message):
    return {'FILE': filename, 'CLASS': classname,
            'METHOD': methodname, 'Message': message}
