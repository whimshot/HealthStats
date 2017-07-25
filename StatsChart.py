"""StatsChart class."""
import logging
import logging.handlers

import matplotlib
from AdaData import AdaData
from Adafruit_IO import MQTTClient
from HSConfig import config
from HSLogger import HostnameFilter

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa
from matplotlib.ticker import MultipleLocator  # noqa

matplotlib.rc('lines', linewidth=0.75, markersize=4,
              linestyle='-', marker='.')
matplotlib.rc('grid', linestyle='-.', linewidth=0.5, alpha=0.5)
matplotlib.rc('legend', framealpha=0.5, loc='upper right')

AIO_KEY = config.get('Adafruit', 'aio_key')
AIO_ID = config.get('Adafruit', 'aio_id')


class StatsChart(object):
    """Stats charts object."""

    feeds = ['weight', 'diastolic', 'systolic', 'pulse', 'bmi']
    feeds_data = {}     # The data last retrieved from the feeds.

    def __init__(self):
        """
        Initial StatsChart.

        Sets up initial containers for data from io.adafruit.com to
        compare against for changes later.
        """
        try:
            self.logger = \
                logging.getLogger("HealthStats." + __name__)
            self.logger.addFilter(HostnameFilter())
            self.logger.info('creating an instance of StatsChart')
            self.client = MQTTClient(AIO_ID, AIO_KEY)
            self.client.on_connect = self.connected
            self.client.on_disconnect = self.disconnected
            self.client.on_message = self.message
            self.client.connect()

            for feed in self.feeds:
                self.feeds_data[feed] = AdaData(feed)
                self.logger.debug("Getting data from io.adatfruit.com"
                                  + " for {0}.".format(feed))
                self.feeds_data[feed].get_data()

            self.logger.info('Getting StatsChart instance up and running.')
            self.client.loop_background()
            self.draw_chart()
        except Exception:
            self.logger.exception('StatsChart instantiation failed.')

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
        self.logger.info('Feed: {0} received new data: {1}'.format(feed_id,
                                                                   payload))
        self.draw_chart()

    def draw_chart(self):
        """Make the stats chart image."""
        try:
            self.logger.debug('Building new image.')
            self.feeds_data['weight'].get_data()
            self.feeds_data['systolic'].get_data()
            self.feeds_data['diastolic'].get_data()
            self.feeds_data['pulse'].get_data()
            self.feeds_data['bmi'].get_data()
            self.logger.debug('Got new data from Adafruit.')

            fig, (weight_chart, bp_chart) = plt.subplots(2, figsize=(4, 4.8))
            bmi_major_locator = MultipleLocator(1)
            bp_minor_locator = MultipleLocator(2)
            weight_minor_locator = MultipleLocator(.2)

            bp_chart.plot(self.feeds_data['systolic'].dates,
                          self.feeds_data['systolic'].data,
                          label='Systolic')
            bp_chart.plot(self.feeds_data['diastolic'].dates,
                          self.feeds_data['diastolic'].data,
                          label='Diastolic')
            bp_chart.plot(self.feeds_data['pulse'].dates,
                          self.feeds_data['pulse'].data,
                          label='Pulse')
            bp_chart.set_ylabel('Blood Pressure (mmHg)\nPulse (BPM)')
            bp_chart.tick_params(axis='y')

            weight_chart.plot(self.feeds_data['weight'].dates,
                              self.feeds_data['weight'].data, 'C0')
            weight_chart.set_ylabel('Weight (Kg)',
                                    fontsize='9',
                                    color='C0')
            weight_chart.tick_params(axis='y',
                                     colors='C0')

            bmi_chart = weight_chart.twinx()
            bmi_chart.yaxis.set_major_locator(bmi_major_locator)
            bmi_chart.plot(self.feeds_data['bmi'].dates,
                           self.feeds_data['bmi'].data, 'C1')
            bmi_chart.set_ylabel('BMI',
                                 fontsize='9',
                                 color='C1')
            bmi_chart.tick_params(axis='y',
                                  colors='C1')

            for ax in fig.axes:
                matplotlib.pyplot.sca(ax)
                plt.xticks(rotation=45)
                ax.tick_params(direction='out', top='off',
                               labelsize='8')
                ax.spines['top'].set_visible(False)
            fig.tight_layout()
            fig.savefig('SmallCharts.png', dpi=100)

            plt.clf()

            # Larger version of the BP Chart.

            fig, bp_chart = plt.subplots(1, figsize=(8, 4.8))
            bp_chart.yaxis.set_minor_locator(bp_minor_locator)
            bp_chart.plot(self.feeds_data['systolic'].dates,
                          self.feeds_data['systolic'].data,
                          label='Systolic')
            bp_chart.plot(self.feeds_data['diastolic'].dates,
                          self.feeds_data['diastolic'].data,
                          label='Diastolic')
            bp_chart.plot(self.feeds_data['pulse'].dates,
                          self.feeds_data['pulse'].data,
                          label='Pulse')
            bp_chart.grid(which='major')
            bp_chart.yaxis.grid(which='minor')
            bp_chart.set_ylabel('Blood Pressure (mmHg)\nPulse (BPM)')
            bp_chart.tick_params(axis='y', which='both')
            bp_chart.legend()

            for ax in fig.axes:
                matplotlib.pyplot.sca(ax)
                plt.xticks(rotation=45)
                ax.tick_params(direction='out', top='off',
                               labelsize='8')
                ax.spines['top'].set_visible(False)
            fig.tight_layout()
            fig.savefig('BPChart.png', dpi=100)

            plt.clf()

            fig, weight_chart = plt.subplots(1, figsize=(8, 4.8))
            weight_chart.yaxis.set_minor_locator(weight_minor_locator)
            wc = weight_chart.plot(self.feeds_data['weight'].dates,
                                   self.feeds_data['weight'].data,
                                   'C0', label='Weight (Kg)')
            weight_chart.set_ylabel('Weight (Kg)',
                                    fontsize='9',
                                    color='C0')
            weight_chart.tick_params(axis='y',
                                     colors='C0',
                                     which='both')
            weight_chart.grid(which='major')
            weight_chart.yaxis.grid(which='minor')

            bmi_chart = weight_chart.twinx()
            bmi_chart.yaxis.set_major_locator(bmi_major_locator)
            bc = bmi_chart.plot(self.feeds_data['bmi'].dates,
                                self.feeds_data['bmi'].data,
                                'C1', label='BMI')
            bmi_chart.set_ylabel('BMI',
                                 fontsize='9',
                                 color='C1')
            bmi_chart.tick_params(axis='y',
                                  colors='C1')

            charts = wc + bc
            labels = [chart.get_label() for chart in charts]

            for ax in fig.axes:
                matplotlib.pyplot.sca(ax)
                plt.xticks(rotation=45)
                ax.tick_params(direction='out', top='off',
                               labelsize='8')
                ax.spines['top'].set_visible(False)

            weight_chart.legend(charts, labels)

            fig.tight_layout()
            fig.savefig('WeightChart.png', dpi=100)

            plt.clf()

        except Exception:
            self.logger.exception('Failed to draw new charts.')


if __name__ == '__main__':
    StatsChart().draw_chart()
