"""A monky that watches a file."""
import os


class FileMonkey(object):
    """A monkey that watches files."""

    def __init__(self, filename):
        """Make that monkey."""
        self._cached_stamp = 0
        self.filename = filename

    def ook(self):
        """Train that monkey."""
        try:
            stamp = os.stat(self.filename).st_mtime
            if stamp != self._cached_stamp:
                self._cached_stamp = stamp
                return True
            else:
                return False
        except ValueError:
            return False
