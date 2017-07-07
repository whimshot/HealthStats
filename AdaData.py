"""Get data from io.adafruit.com."""
from datetime import datetime
from pytz import timezone
from Adafruit_IO import Client
from AdafruitIOKey import AIO_KEY


class AdaData(object):
    """AdaData object."""

    aio = Client(AIO_KEY)

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
            zdate = str(entry.created_at).replace('Z', '+0000')
            edate = (datetime
                     .strptime(zdate, "%Y-%m-%dT%H:%M:%S%z")
                     .astimezone(timezone('US/Eastern')))
            self.dates.append(edate)
