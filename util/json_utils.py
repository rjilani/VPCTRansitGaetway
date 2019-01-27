import json
import datetime
import inspect
from util.log_utils import formatmessage

# Uitlity class to print, read and write Json
class JsonUtil(object):

    def __init__(self, logging):
        self.filename = __file__.split('/')[-1]
        self.classname = self.__class__.__name__
        self.logging = logging

    def pretty_json(self, response):
        methodname = inspect.stack()[0][3]
        try:
            message = formatmessage(self.filename, self.classname, methodname, "converting object to pretty json")
            self.logging.debug(message)
            return json.dumps(response, indent=4, sort_keys=True, default=JsonUtil.dateconverter)
        except Exception as exc:
            message = formatmessage(self.filename, self.classname, methodname, str(exc))
            self.logging.error(message)

    def write_json_file(self, filelocation, text):
        methodname = inspect.stack()[0][3]
        try:
            with open(filelocation, 'w', encoding='utf-8') as f:
                f.write(text)
                message = formatmessage(self.filename, self.classname, methodname, "writing to file")
                self.logging.debug(message)
        except Exception as exc:
            message = formatmessage(self.filename, self.classname, methodname, str(exc))
            self.logging.error(message)

    def read_json_file(self, filelocation):
        methodname = inspect.stack()[0][3]
        try:
            with open(filelocation) as f:
                data = json.load(f)
                message = formatmessage(self.filename, self.classname, methodname, "reading from the file")
                self.logging.debug(message)
                return data
        except Exception as exc:
            message = formatmessage(self.filename, self.classname, methodname, str(exc))
            self.logging.error(message)

    @staticmethod
    def dateconverter(o):
        if isinstance(o, datetime.datetime) or isinstance(o, datetime.date):
            return o.__str__()
