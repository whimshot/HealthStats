"""Get data from io.adafruit.com."""
import logging
import logging.handlers
from datetime import datetime

from Adafruit_IO import Client, MQTTClient
from dateutil import tz
from hsconfig import config
from hslogger import HostnameFilter

AIO_KEY = config.get('Adafruit', 'aio_key')
AIO_ID = config.get('Adafruit', 'aio_id')


class AdaFeed(object):
    """AdaData object."""

    aio = Client(AIO_KEY)
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    def __init__(self, feed):
        """Create new AdaData instance."""
        try:
            self.logger = logging.getLogger('HealthStats.'
                                            + self.__class__.__name__)
            self.logger.addFilter(HostnameFilter())
            self.feed = feed
            self.data = []
            self.dates = []
            self.client = MQTTClient(AIO_ID, AIO_KEY)
            self.client.on_connect = self.connected
            self.client.on_disconnect = self.disconnected
            self.client.on_message = self.message
            self.client.connect()
            self.logger.debug('Data instance for {0}.'.format(feed))
            self.client.loop_background()
        except Exception:
            self.logger.exception('Failed to instantiate AdaFeed.')

    def __eq__(self, other):
        """`Are they the same?` Is the question."""
        self.logger.debug('Comparing two instances of AdaFeed.')
        return self.__dict__ == other.__dict__

    def get_data(self):
        """Get data from io.adatruit.com."""
        try:
            self.logger.debug('Querying {0}.'.format(self.feed))
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
            self.logger.debug('Retrieved data from {0}.'.format(self.feed))
        except Exception:
            self.logger.exception('Caught exception.')

    def connected(self, client):
        """Called when connection to io.adafruit.com is successful."""
        # Subscribe to changes for the feeds listed.
        self.logger.debug('Connected to Adafruit, subscribing to feeds.')
        try:
            self.logger.debug('Subscribing to {0} feed.'.format(self.feed))
            self.client.subscribe(self.feed)
        except Exception:
            self.logger.exception('Failed to subscribe to feed.')

    def disconnected(self, client):
        """Called when disconnected from io.adafruit.com."""
        self.logger.info('Disconnected from Adafruit IO!')

    def message(self, client, feed_id, payload):
        """Called when a subscribed feed gets new data."""
        try:
            self.logger.debug("Feed: {0} received".format(feed_id)
                              + " new data: {0}".format(payload))
            self.get_data()
        except Exception:
            raise
        finally:
            pass


class AdaData():
    """This is where we store the data from all the feeds."""

    def __init__(self):
        """
        Initial AdaData.

        Sets up initial containers for data from io.adafruit.com to
        compare against for changes later.
        """
        try:
            self.feeds = ['weight', 'diastolic', 'systolic', 'pulse', 'bmi']
            self.feeds_data = {}     # The data last retrieved from the feeds.
            self.filename = ""
            self.logger = \
                logging.getLogger('HealthStats.'
                                  + self.__class__.__name__)
            self.logger.addFilter(HostnameFilter())
            self.logger.info('creating an instance of ChartMaker')
            self.client = MQTTClient(AIO_ID, AIO_KEY)
            self.client.on_connect = self.connected
            self.client.on_disconnect = self.disconnected
            self.client.on_message = self.message

            for feed in self.feeds:
                self.feeds_data[feed] = AdaFeed(feed)
                self.logger.debug("Getting data from io.adatfruit.com"
                                  + " for {0}.".format(feed))
                self.feeds_data[feed].get_data()

            self.client.connect()
            self.logger.debug('Getting AdaData instance up and running.')
            self.client.loop_background()
        except Exception:
            self.logger.exception('AdaData instantiation failed.')

    def get_data(self):
        """Retrieve data from io.adafruit.com."""
        try:
            for feed in self.feeds:
                self.feeds_data[feed].get_data()
        except Exception:
            raise
        finally:
            pass

    def connected(self, client):
        """Called when connection to io.adafruit.com is successful."""
        # Subscribe to changes for the feeds listed.
        self.logger.debug('Connected to Adafruit, subscribing to feeds.')
        try:
            for feed in self.feeds:
                self.logger.debug('Subscribing to {0} feed.'.format(feed))
                self.client.subscribe(feed)
        except Exception:
            self.logger.exception('Failed to subscribe to feed.')

    def disconnected(self, client):
        """Called when disconnected from io.adafruit.com."""
        self.logger.info('Disconnected from Adafruit IO!')

    def message(self, client, feed_id, payload):
        """Called when a subscribed feed gets new data."""
        try:
            self.logger.debug("Feed: {0} received".format(feed_id)
                              + " new data: {0}".format(payload))
            self.feeds_data[feed_id].get_data()
            if (feed_id in ('weight', 'bmi')):
                self.weight_chart()
            if (feed_id in ('systolic', 'diastolic', 'pulse')):
                self.bp_chart()
            if (feed_id in ('systolic', 'diastolic', 'pulse',
                            'weight', 'bmi')):
                self.small_charts()
        except Exception:
            raise
        finally:
            pass


if __name__ == '__main__':
    ad = AdaData()
