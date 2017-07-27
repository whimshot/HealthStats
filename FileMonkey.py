"""A monkey that watches a file."""
import logging
import logging.handlers
import os

from HSLogger import HostnameFilter


class FileMonkey(object):
    """A monkey that watches files."""

    def __init__(self, filename):
        """Set up file watching monkey."""
        self.logger = logging.getLogger('HealthStats.'
                                        + self.__class__.__name__)
        self.logger.addFilter(HostnameFilter())
        self.logger.info('New FileMonkey watching {0}.'.format(filename))
        self._cached_stamp = 0
        self.filename = filename

    def ook(self):
        """Check if the file been changed."""
        try:
            stamp = os.stat(self.filename).st_mtime
            if stamp != self._cached_stamp:
                self._cached_stamp = stamp
                self.logger.debug('{0} has changed.'.format(self.filename))
                return True
            else:
                self.logger.debug('{0} has not changed.'.format(self.filename))
                return False
        except Exception:
            self.logger.exception('Problem with file, caught exception.')
            return True
