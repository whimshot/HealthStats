"""Logging filters for local use."""
import logging
import logging.handlers
import platform
from HSConfig import config


class HostnameFilter(logging.Filter):
    """Filter to insert a hostname record."""

    def filter(self, record):
        """Filter function."""
        hostname = platform.node().split('.')[0]
        record.hostname = hostname
        return 1


MAXLOGSIZE = config.getint('Logging', 'MAXLOGSIZE')

# create logger
logger = logging.getLogger('HealthStats')
# logger.setLevel(logging.INFO)
logger.setLevel(logging.INFO)
logger.addFilter(HostnameFilter())
# create file handler which logs even debug messages
logger_fh = logging.handlers.RotatingFileHandler('HealthStats.log',
                                                 maxBytes=MAXLOGSIZE,
                                                 backupCount=8)
logger_fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
logger_ch = logging.StreamHandler()
logger_ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
logger_formatter = logging.Formatter('%(asctime)s'
                                     + ' %(hostname)s'
                                     + ' %(levelname)s'
                                     + ' %(name)s[%(process)d]'
                                     + ' %(message)s')
logger_fh.setFormatter(logger_formatter)
logger_ch.setFormatter(logger_formatter)
# add the handlers to the logger
logger.addHandler(logger_fh)
logger.addHandler(logger_ch)
