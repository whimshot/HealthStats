"""Get data from io.adafruit.com."""
from datetime import datetime
from dateutil import tz
from Adafruit_IO import Client
from AdafruitIOKey import AIO_KEY
import logging
from LogFilters import HostnameFilter


# create logger
module_logger = logging.getLogger('HealthStats.AdaData')
module_logger.addFilter(HostnameFilter())


class AdaData(object):
    """AdaData object."""

    aio = Client(AIO_KEY)
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    def __init__(self, feed):
        """Create new AdaData instance."""
        try:
            self.logger = logging.getLogger('HealthStats.AdaData.AdaData')
            self.logger.addFilter(HostnameFilter())
            self.feed = feed
            self.data = []
            self.dates = []
            self.logger.info('AdaData instance for {0} feed.'.format(feed))
        except Exception:
            self.logger.exception('Failed to instantiate AdaData.')

    def __eq__(self, other):
        """`Are they the same?` Is the question."""
        self.logger.debug('Comparing two instances of AdaData.')
        return self.__dict__ == other.__dict__

    def get_data(self):
        """Get data from io.adatruit.com."""
        try:
            self.logger.debug('Querying {0} feed.'.format(self.feed))
            self.data = []
            self.dates = []
            feed_data = self.aio.data(self.feed)
            self.logger.debug('Parsing dates from {0}'.format(self.feed))
            for entry in feed_data:
                self.data.append(entry.value)
                self.logger.debug('Appended {0}'.format(entry.value))
                utc = datetime.strptime(entry.created_at, '%Y-%m-%dT%H:%M:%SZ')
                utc = utc.replace(tzinfo=self.from_zone)
                local = utc.astimezone(self.to_zone)
                self.dates.append(local)
                self.logger.debug('Appended {0}'.format(local))
            self.logger.info('Retrieved data from {0} feed.'.format(self.feed))
        except Exception:
            self.logger.exception('Caught exception.')
