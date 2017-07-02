"""Get data from io.adafruit.com."""
from adafruitiokey import aoi_key
from datetime import datetime
from Adafruit_IO import Client


class AdaData(object):
    """AdaData object."""

    aio = Client(aoi_key)

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
        feed_data = self.aio.data(self.feed)
        for entry in feed_data:
            self.data.append(entry.value)
            date = str(entry.created_at).replace('Z', '+0000')
            self.dates.append(datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z"))
