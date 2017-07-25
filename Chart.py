""""A smart chart class.

The chart class is an extension of the kivy image class with the ability
to subscribe to data feeds, redraw itself and reload once a new image
has been generated.
"""
from Adafruit_IO import MQTTClient
from AdaData import AdaData
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.widget import Widget
import logging
import logging.handlers
import time
from HSLogger import logger, HostnameFilter
from HSConfig import config
import matplotlib
matplotlib.use('Agg')
from matplotlib import ticker as tckr
from matplotlib import pyplot as plt

AIO_KEY = config.get('Adafruit', 'aio_key')
AIO_ID = config.get('Adafruit', 'aio_id')
matplotlib.rc('lines', linewidth=0.75, markersize=4,
              linestyle='-', marker='.')
matplotlib.rc('grid', linestyle='-.', linewidth=0.5, alpha=0.5)
matplotlib.rc('legend', framealpha=0.5, loc='upper right')


class Chart(Image):
    """The basic Chart class we will build off from here."""

    feeds = []          # The list of feeds the chart is subscribed to.
    feeds_data = {}     # The data last retrieved from the feeds.
    feeds_changed = []  # Truthiness to record when feeds are updated.
    filename = ""

    def __init__(self, **kwargs):
        """Chart object instance."""
        super(Chart, self).__init__(**kwargs)
        try:
            self.logger = \
                logging.getLogger('HealthStats.' + __name__)
            self.logger.addFilter(HostnameFilter())
            self.logger.info('creating an instance of StatsChart')
            self.client = MQTTClient(AIO_ID, AIO_KEY)
            self.client.on_connect = self.connected
            self.client.on_disconnect = self.disconnected
            self.client.on_message = self.message
            self.client.connect()
            self.client.loop_background()
        except Exception:
            self.logger.exception('Chart instantiation failed.')
        finally:
            pass

    def build(self):
        """Builder for chart object."""
        self.filename = str(self.source)
        try:
            logger.debug("Building new chart {0}.".format(self.filename))
            for feed in self.feeds:
                self.client.subscribe(feed)
                self.logger.debug("Subscribed to {0}.".format(feed))
        except Exception:
            logger.exception("Caught exception.")
        finally:
            pass

    def connected(self, client):
        """Called when connection to io.adafruit.com is successful."""
        # Subscribe to changes for the feeds listed.
        self.logger.info('Connected to Adafruit, subscribing to feeds.')
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
            self.logger.debug("Feed: {0} received new data: ".format(feed_id)
                              + "{0}".format(payload))
            self.feeds_data[feed_id].get_data()
            time.sleep(3)
            self.reload()
        except Exception:
            raise
        finally:
            pass


class WeightChart(Chart):
    """Class for the WeightChart image."""

    pass


class BPChart(Chart):
    """Class for the BPChart image."""

    pass


class SmallCharts(Chart):
    """Class for the SmallCharts image."""

    pass


class ChartDemo(Widget):
    """Demo for testing charts."""


class ChartApp(App):
    """Kivy App Class for ChartDemo."""

    def build(self):
        """Build function for ChartDemo kivy app."""
        logger.info('Starting ChartDemoApp.')
        cd = ChartDemo()
        cd.weightchart.build()
        cd.bpchart.build()
        cd.smallcharts.build()
        return cd


if __name__ == '__main__':
    ChartApp().run()
