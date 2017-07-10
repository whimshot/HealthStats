"""StatsChart class."""
from AdaData import AdaData
from AdafruitIOKey import AIO_KEY, AIO_ID
import matplotlib
from Adafruit_IO import MQTTClient
from LogFilters import HostnameFilter
import logging
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# create logger
module_logger = logging.getLogger('HealthStats.StatsChart')
module_logger.addFilter(HostnameFilter())


class StatsChart(object):
    """Stats charts object."""

    feeds = ['weight', 'diastolic', 'systolic', 'pulse', 'bmi']

    def __init__(self):
        """
        Initial StatsChart.

        Sets up initial containers for data from io.adafruit.com to
        compare against for changes later.
        """
        self.logger = logging.getLogger('HealthStats.StatsChart.StatsChart')
        self.logger.addFilter(HostnameFilter())
        self.logger.info('creating an instance of StatsChart')
        self.client = MQTTClient(AIO_ID, AIO_KEY)
        self.client.on_connect = self.connected
        self.client.on_disconnect = self.disconnected
        self.client.on_message = self.message
        self.client.connect()

        self.weight = AdaData('weight')
        self.systolic = AdaData('systolic')
        self.diastolic = AdaData('diastolic')
        self.pulse = AdaData('pulse')

        self.logger.info('Getting StatsChart instance up and running.')
        self.client.loop_background()
        self.draw_chart()

    def connected(self, client):
        """Called when connection to io.adafruit.com is successful."""
        # Subscribe to changes for the feeds listed.
        self.logger.info('Connected to Adafruit, subscribing to feeds.')
        for feed in self.feeds:
            self.logger.info('Subscribing to {0} feed.'.format(feed))
            self.client.subscribe(feed)

    def disconnected(self, client):
        """Called when disconnected from io.adafruit.com."""
        self.logger.info('Disconnected from Adafruit IO!')

    def message(self, client, feed_id, payload):
        """Called when a subscribed feed gets new data."""
        self.logger.info('Feed: {0} received new data: {1}'.format(feed_id,
                                                                   payload))
        self.draw_chart()

    def draw_chart(self):
        """Make the stats chart image."""
        try:
            self.logger.info('Building new image.')
            self.weight.get_data()
            self.systolic.get_data()
            self.diastolic.get_data()
            self.pulse.get_data()
            self.logger.debug('Got new data from Adafruit.')

            fig, (weight_chart, bp_chart) = plt.subplots(2, figsize=(4, 4.8))

            bp_chart.plot(self.systolic.dates, self.systolic.data, 'b.-')
            bp_chart.plot(self.diastolic.dates, self.diastolic.data, 'r.-')
            bp_chart.set_ylabel('Blood Pressure\n(mmHg)', fontsize='8')

            weight_chart.plot(self.weight.dates, self.weight.data, 'g.-')
            weight_chart.set_ylabel('Weight (Kg)', fontsize='8')
            weight_chart.set_ylim(120, 150)

            for ax in fig.axes:
                matplotlib.pyplot.sca(ax)
                plt.xticks(rotation=45)
                ax.tick_params(direction='out', top='off', right='off',
                               labelsize='8')
                start, end = ax.get_xlim()
                ax.spines['right'].set_visible(False)
                ax.spines['top'].set_visible(False)
                ax.grid(axis='y', linestyle='-.')

            fig.tight_layout()
            fig.savefig('StatsCharts.png', dpi=100)

            plt.clf()

        except Exception:
            self.logger.exception('Caught exception.')
