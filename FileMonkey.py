"""A monkey that watches a file."""
import os
import logging


# create logger
module_logger = logging.getLogger('HealthStats.FileMonkey')


class FileMonkey(object):
    """A monkey that watches files."""

    def __init__(self, filename):
        """Make that monkey."""
        self.logger = logging.getLogger('HealthStats.FileMonkey.FileMonkey')
        self.logger.info('New FileMonkey watching {0}.'.format(filename))
        self._cached_stamp = 0
        self.filename = filename

    def ook(self):
        """Train that monkey."""
        try:
            stamp = os.stat(self.filename).st_mtime
            if stamp != self._cached_stamp:
                self._cached_stamp = stamp
                self.logger.debug('{0} has changed.'.format(self.filename))
                return True
            else:
                self.logger.debug('{0} has not changed.'.format(self.filename))
                return False
        except (ValueError) as ve:
            self.logger.debug('Caught error {0}'.format(ve))
            return False
        except (OSError) as oe:
            self.logger.debug('Caught error {0}'.format(oe))
            return True
