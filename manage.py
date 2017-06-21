#!/usr/bin/env python2.7

""" File managing all commands to manage the expert-octo-fortnight

LICENSE: TODO

COMMANDS:
    devserver             Run the application using dev
    createdb              Create the database
    migratedb             Migrates and upgrads the database
    shell                 Starts a python shell in app context
    parseOpps             Parses the 3 PDF files in /app/testing_data/ and populates the DB

USAGE:
    manage.py devserver [-p NUM] [-l DIR] [--config_prod]
    manage.py createdb [--config_prod]
    manage.py migratedb [--config_prod]
    manage.py shell [--config_prod]
    manage.py parseOpps [--config_prod]

OPTIONS:
    --config_prod         Load the production configurations instead of development
    -p NUM --port=NUM     Flask will listen on this port number. default: 5000
    -l DIR --log_dir=DIR  Log all statements to files in this directory instead of stdout.

"""
# Python imports
from functools import wraps
from pydoc import locate
import logging
import logging.handlers
import os
import signal
import sys
import os.path
from docopt import docopt

# Flask and database imports
import flask
from flask_script import Shell
from migrate.versioning import api
from migrate.exceptions import InvalidRepositoryError, DatabaseAlreadyControlledError
import imp

from sqlalchemy import create_engine, or_
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Application imports
from app.application import create_app, get_config
from app.extensions import db
import app.models

OPTIONS = docopt(__doc__) if __name__ == '__main__' else dict()

class CustomFormatter(logging.Formatter):
    """ Adds the custom formatter for logging (the character at the beginning of the log) """
    LEVEL_MAP = {logging.FATAL: 'F', logging.ERROR: 'E', logging.WARN: 'W', logging.INFO: 'I', logging.DEBUG: 'D'}

    def format(self, record):
        record.levelletter = self.LEVEL_MAP[record.levelno]
        return super(CustomFormatter, self).format(record)

def setup_logging(name = None):
    """ Google-Style logging (no idea what this means -- Rodda)

    name: Appends this string to the log file filename
    """

    log_to_disk = False
    if OPTIONS['--log_dir']:
        if not os.path.isdir(OPTIONS['--log_dir']):
            print('ERROR: Directory {} does not exist.'.format(OPTIONS['--log_dir']))
            sys.exit(1)
        if not os.access(OPTIONS['--log_dir'], os.W_OK):
            print('ERROR: No permission to write to directory {}.'.format(OPTIONS['--log_dir']))
            sys.exit(1)
        log_to_disk = True

    fmt = '%(levelletter)s %(asctime)s.%(msecs).03d %(process)d %(filename)s:%(lineno)d] %(message)s'
    datefmt = '%m%d %H:%M:%S'
    formatter = CustomFormatter(fmt, datefmt)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.ERROR if log_to_disk else logging.DEBUG)
    console_handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(console_handler)

    if log_to_disk:
        file_name = os.path.join(OPTIONS['--log_dir'], 'app_{}.log'.format(name))
        file_handler = logging.handlers.TimedRotatingFileHandler(file_name, when='d', backupCount = 7)
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)

def log_messages(app, port):
    """ Log messages common to dev and production servers """

    log = logging.getLogger(__name__)
    log.info('Server is running at https://0.0.0.0:{}/'.format(port))
    log.info('Flask version: {}'.format(flask.__version__))
    log.info('DEBUG: {}'.format(app.config['DEBUG']))
    log.info('STATIC_FOLDER: {}'.format(app.static_folder))

def parse_options():
    """ Parses command line options for Flask

    Returns:
    Config instance to pass into create_app()
    """

    if OPTIONS['--config_prod']:
        config_class_string = 'app.config.Production'
    else:
        config_class_string = 'app.config.Testing'
    config_obj = get_config(config_class_string)

    return config_obj

def command(func):
    """ Decorator that registers the chosen command/function.

    Instead of Flask-Script

    func: the function to decorate
    """
    @wraps(func)
    def wrapped():
        return func()

    if func.__name__ not in OPTIONS:
        raise KeyError('Cannot register {}, not mentioned in docstring/docopt.'.format(func.__name__))
    if OPTIONS[func.__name__]:
        command.chosen = func

    return wrapped

@command
def devserver():
    """ Starts the development server """
    setup_logging('devserver')
    app = create_app(parse_options())
    log_messages(app, OPTIONS['--port'])
    app.run(host = '0.0.0.0', port = int(OPTIONS['--port']))

@command
def createdb():
    """ Creates the database

    It creates the app based on the flags passed into the script, thus the correct configuration is loaded
    """

    config_class = parse_options()

    if not os.path.exists(config_class.SQLALCHEMY_DATABASE_LOCATION):
        os.makedirs(config_class.SQLALCHEMY_DATABASE_LOCATION)

    app = create_app(parse_options())

    try:
        with app.app_context():
            db.create_all()
            if not os.path.exists(config_class.SQLALCHEMY_MIGRATE_REPO):
                api.create(config_class.SQLALCHEMY_MIGRATE_REPO, 'database repository')
                api.version_control(config_class.SQLALCHEMY_DATABASE_URI, config_class.SQLALCHEMY_MIGRATE_REPO)
            else:
                api.version_control(config_class.SQLALCHEMY_DATABASE_URI, config_class.SQLALCHEMY_MIGRATE_REPO, api.version(config_class.SQLALCHEMY_MIGRATE_REPO))

    except DatabaseAlreadyControlledError:
        print 'WARNING: This database already exists'

@command
def migratedb():
    """ Migrates the database

    It creates the app based on the flags passed into the script, thus the correct configuration is loaded
    """

    config_class = parse_options()

    if not os.path.exists(config_class.SQLALCHEMY_DATABASE_LOCATION):
        os.makedirs(config_class.SQLALCHEMY_DATABASE_LOCATION)

    app = create_app(parse_options())

    try:
        with app.app_context():
            v = api.db_version(config_class.SQLALCHEMY_DATABASE_URI, config_class.SQLALCHEMY_MIGRATE_REPO)

            migration = config_class.SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))

            tmp_module = imp.new_module('old_model')
            old_model = api.create_model(config_class.SQLALCHEMY_DATABASE_URI, config_class.SQLALCHEMY_MIGRATE_REPO)

            exec(old_model, tmp_module.__dict__)
            script = api.make_update_script_for_model(config_class.SQLALCHEMY_DATABASE_URI, config_class.SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)

            open(migration, "wt").write(script)
            api.upgrade(config_class.SQLALCHEMY_DATABASE_URI, config_class.SQLALCHEMY_MIGRATE_REPO)

            v = api.db_version(config_class.SQLALCHEMY_DATABASE_URI, config_class.SQLALCHEMY_MIGRATE_REPO)

            print('INFORMATION: New migration saved as ' + migration)
            print('INFORMATION: Current database version: ' + str(v))

    except InvalidRepositoryError:
        print('ERROR: This database does not exist')

@command
def shell():
    setup_logging('shell')
    app = create_app(parse_options())
    app.app_context().push()
    Shell(make_context=lambda: dict(app=app, db=db)).run(no_ipython=False, no_bpython=False)

@command
def parseOpps():
    from PyPDF2 import PdfFileReader
    from app.models.opportunities import Opportunity

    DATA_DIR = "app/static/opp_raw/"
    
    ### GLOBALS ###
    files = ["opp1.pdf", "opp2.pdf", "opp3.pdf"]
    keywords = ["Additional Information", "Schedule of Programs", "List of Academy Locations", "Website", "Application", "Contact", "Contact Information", "Email", "Duration", "Eligibility", "Deadline"]
    oppList = []

    def getNextKwdIndex(splitted, lineNum):
        for line in [x + lineNum + 1 for x in xrange(len(splitted[lineNum+1:]))]:
            indexList = [line for kwd in keywords if kwd in splitted[line]]
            if indexList:
                nextKwdIndex = min(indexList)
                return nextKwdIndex
        return -1

    def parsePDF(filename):
        f = PdfFileReader(open(filename, "rb"))
        # print how many pages input1 has:
        print "%s has %d pages." % (filename, f.getNumPages())
    
        #start from page 2 (0 is title, 1 is ToC, 2-3 are general opp links)
        numPages = f.getNumPages() - 4
        for pageNum in [x+4 for x in xrange(numPages)]:
            pageObj = f.getPage(pageNum)
            pageObj.compressContentStreams()
            pageText = pageObj.extractText().strip()
            splitted = pageText.split('\n')[1:] #first line is page num
        
            #fix dumb syntactical things
            lineNum = 0
            while lineNum < len(splitted):
                if splitted[lineNum] == '-':
                    splitted[lineNum-1] += '-' + splitted[lineNum+1]
                    splitted.pop(lineNum)
                    splitted.pop(lineNum) #lineNum+1 becomes lineNum after first pop
                elif splitted[lineNum] in ['', ' ']:
                    splitted.pop(lineNum)
                else:
                    lineNum += 1
                
            #pass 2: parse opps
            currentOpp = {}
            for lineNum in xrange(len(splitted)):
                if "Details:" in splitted[lineNum]: #opp has been located, YEET
                    #refresh currentOpp
                    oppList.append(currentOpp)
                    currentOpp = {}
                    currentOpp["Name"] = splitted[lineNum-1]
                    nextKwdIndex = getNextKwdIndex(splitted, lineNum)
                    if nextKwdIndex == -1:
                        nextKwdIndex = len(splitted)
                    currentOpp["Details"] = reduce(lambda x,y: x.strip() + ' ' + y.strip()if len(y)<3 else x+y, splitted[lineNum+1:nextKwdIndex]) #dont ask
                elif splitted[lineNum].strip() in keywords: #if its a keyword other than "Details:"
                    if "Name" in currentOpp and currentOpp["Name"] == "AIDS WALK":
                        print splitted[lineNum: lineNum+10]
                    nextKwdIndex = getNextKwdIndex(splitted, lineNum)
                    if "Details:" in splitted[nextKwdIndex]:
                        nextKwdIndex -= 1 #dont include the title of the next opp
                    elif nextKwdIndex == -1:
                        nextKwdIndex = len(splitted)
                    currentOpp[splitted[lineNum].strip(': ')] = reduce(lambda x,y: x.strip() + ' ' + y.strip()if len(y)<3 else x+y, splitted[lineNum+1:nextKwdIndex]) #dont ask


    app = create_app(get_config('app.config.Testing'))
    app.app_context().push()
    for filename in files:
        parsePDF(DATA_DIR + filename)
    for opp in oppList:
#        print "\n" * 2 + str(opp)
        
        if not opp or "Name" not in opp or "Details" not in opp:
            continue
        o = Opportunity(name = opp["Name"], description = opp["Details"])
        #initialize
        o.details = ""
        o.link = ""
        o.organization = ""
        o.required_materials = []
        o.deadline = ""
        
        if "Additional Information" in opp:
            o.details += "\nAdditional Information: " + opp["Additional Information"]
        if "Schedule of Programs" in opp:
            o.details += "\nSchedule of Programs: " + opp["Schedule of Programs"]
        if "List of Academy Locations" in opp:
            o.details += "\nList of Academy Locations: " + opp["List of Academy Locations"]
        if "Website" in opp:
            o.link += "\n" + opp["Website"]
        if "Application" in opp:
            o.link += "\n" + opp["Application"]
        if "Contact" in opp:
            o.organization += "\n" + opp["Contact"]
        if "Contact Information" in opp:
            o.organization += "\n" + opp["Contact Information"]
        if "Email" in opp:
            o.organization += "\n" + opp["Email"]
        #skip duration for now cuz its weird
        if "Eligibility" in opp:
            o.required_materials = [opp["Eligibility"]]
        if "Deadline" in opp:
            o.deadline = opp["Deadline"]
        #print "added opp: %s" % o.name
        db.session.add(o)
    db.session.commit()  

    
if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda *_: sys.exit(0)) # Catches SIGINT and exits "theoretically" nicely

    if OPTIONS['--port'] and not OPTIONS['--port'].isdigit():
        print('ERROR: Port should be a number.')
        sys.exit(1)
    getattr(command, 'chosen')()
