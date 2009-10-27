from xml.sax.handler import ContentHandler
from datetime import datetime
from xml.sax import make_parser
import util.datetimeutils

import sys

class LabelHandler(ContentHandler):
    def __init__(self, build):
        self.build = build

    def startElement(self, name, attrs):
        if (name == "property" and attrs['name'] == 'label') :
            self.build.number = attrs["value"];

class ProjNameHandler(ContentHandler):
    def __init__(self, build):
        self.build = build

    def startElement(self, name, attrs):
        if (name == "property" and attrs['name'] == 'projectname') :
            self.build.name = attrs["value"];

class TimeStampHandler(ContentHandler):
    def __init__(self, build):
        self.build = build

    def startElement(self, name, attrs):
        if (name == "property" and attrs['name'] == 'cctimestamp') :
            self.build.start_time = datetime.strptime(attrs["value"], "%Y%m%d%H%M%S") ;

class ResultHandler(ContentHandler):
    def __init__(self, build):
        self.build = build

    def startElement(self, name, attrs):
        if (name == "property" and attrs['name'] == 'logfile') :
            self.build.is_passed = attrs["value"].find('Lbuild') > -1

class LastPassHandler(ContentHandler):
    def __init__(self, build):
        self.build = build

    def startElement(self, name, attrs):
        if (name == "property" and attrs['name'] == 'lastsuccessfulbuild') :
            self.build.last_pass = datetime.strptime(attrs["value"], "%Y%m%d%H%M%S")

class BuildTimeHandler(ContentHandler):
    def __init__(self, build):
        self.build = build

    def startElement(self, name, attrs):
        if (name == "build") :
            build_time = util.datetimeutils.evaluate_time_to_seconds(attrs["time"])
            self.build.build_time = build_time

class MultipleHandlers(ContentHandler):
    def __init__(self, build):
        self.handlers = [LabelHandler(build), ProjNameHandler(build), TimeStampHandler(build), ResultHandler(build),
                         LastPassHandler(build), BuildTimeHandler(build)]

    def startElement(self, name, attrs):
        for handler in self.handlers :
            handler.startElement(name, attrs)







