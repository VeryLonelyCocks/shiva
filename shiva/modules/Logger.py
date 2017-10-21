"""
https://docs.python.org/3/library/logging.html
"""
import logging
from .Hawk import Hawk


class Logger:

    format_console = "%(filename)-20s:%(lineno)-4s%(funcName)20s()\t\t%(message)s"
    level=logging.DEBUG

    def __init__(self, core):
        self.core = core

        self.logger = logging.getLogger('asyncio')
        self.logger.setLevel(self.level)

        logging.basicConfig(level=self.level, format=self.format_console)


class LoggerHandlers:

    def add(core, logger, handlers=[]):

        if 'journal' in handlers:
            logger.addHandler(LoggerHandlers.journal('logs/' + core.PARAMS['name'] + '.log'))
            core.logger.info('Logger handler Journal initiated')

        if 'hawk' in handlers:
            logger.addHandler(LoggerHandlers.hawk(core.hawk))
            core.logger.info('Logger handler Hawk initiated')

        if 'db' in handlers:
            logger.addHandler(LoggerHandlers.db(core.db))
            core.logger.info('Logger handler DB initiated')

    def journal(journal_path):
        format_journal = "%(asctime)s %(levelname)s %(message)s"
        handler = logging.FileHandler(journal_path)
        formatter = logging.Formatter(format_journal)
        handler.setFormatter(formatter)
        return handler

    def db(database):
        return LogDBHandler(database)

    def hawk(hawk):
        return LogHawkHandler(hawk)


class LogDBHandler(logging.Handler):

    COLLECTION_LOGS = 'app_logs'

    def __init__(self, db):
        logging.Handler.__init__(self)
        self.table = db[self.COLLECTION_LOGS]

    def emit(self, record):
        new_log_record = {
            # time
            'asctime': record.asctime,

            # error info
            'levelname': record.levelname,
            'message': record.message,
            'exc_text': record.exc_text,

            # error path
            'pathname': record.pathname,
            'filename': record.filename,
            'lineno': record.lineno,
            'module': record.module,
            'funcName': record.funcName,
            'args': record.args,
        }

        self.table.insert_one(new_log_record)


class LogHawkHandler(logging.Handler):

    def __init__(self, hawk):
        logging.Handler.__init__(self)
        self.hawk = hawk

    def emit(self, record):

        if record.exc_info:
            try:
                raise record.exc_info[1]
            except:
                self.hawk.catch()
