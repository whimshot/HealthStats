"""Get data from io.adafruit.com."""
from datetime import datetime
from dateutil import tz
from Adafruit_IO import Client
from AdafruitIOKey import AIO_KEY


class AdaData(object):
    """AdaData object."""

    aio = Client(AIO_KEY)
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    def __init__(self, feed):
        """Create new HealthStats object."""
        self.feed = feed
        self.data = []
        self.dates = []

    def __eq__(self, other):
        """`Are they the same?` Is the question."""
        return self.__dict__ == other.__dict__

    def get_data(self):
        """Get data from io.adatruit.com."""
        self.data = []
        self.dates = []
        feed_data = self.aio.data(self.feed)
        for entry in feed_data:
            self.data.append(entry.value)
            utc = datetime.strptime(entry.created_at, '%Y-%m-%dT%H:%M:%SZ')
            utc = utc.replace(tzinfo=self.from_zone)
            local = utc.astimezone(self.to_zone)
            self.dates.append(local)
