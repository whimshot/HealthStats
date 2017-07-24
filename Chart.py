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
matplotlib.rc('legend', framealpha=0.5, numpoints=2, loc='upper right')



class Chart(Image):
    """The basic Chart class we will build off from here."""

    feeds = []          # The list of feeds the chart is subscribed to.
    feeds_data = {}     # The data last retrieved from the feeds.
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

            self.logger.info('Getting StatsChart instance up and running.')
            self.client.loop_background()
        except Exception:
            self.logger.exception('StatsChart instantiation failed.')
        finally:
            pass

    def build(self):
        """Builder for chart object."""
        self.filename = str(self.source)
        try:
            logger.debug("Building new chart {0}.".format(self.filename))
            for feed in self.feeds:
                self.feeds_data[feed] = AdaData(feed)
                self.feeds_data[feed].get_data()
                self.logger.debug("Got data from io.adatfruit.com"
                                  + " for {0}.".format(feed))
                self.client.subscribe(feed)
                self.logger.debug("Subscribed to {0}.".format(feed))
            self.draw_chart()
        except Exception:
            logger.exception("Caught exception.")
        finally:
            pass

    def draw_chart(self):
        """Make the stats chart image."""
        try:
            pass
        except Exception:
            self.logger.exception('Failed to draw new charts.')

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
            self.logger.info("Feed: {0} received"
                             + " new data: {1}".format(feed_id,
                                                       payload))
            self.feeds_data[feed_id].get_data()
            self.draw_chart()
        except Exception:
            raise
        finally:
            pass


class WeightChart(Chart):
    """Class for the WeightChart image."""

    def draw_chart(self):
        """Make the stats chart image."""
        try:
            self.logger.debug("Drawing chart for {0}.".format(self.filename))
            weight_minor_locator = tckr.MultipleLocator(.2)
            bmi_major_locator = tckr.MultipleLocator(1)
            fig, weight_chart = plt.subplots(1, figsize=(8, 4.8))
            weight_chart.yaxis.set_minor_locator(weight_minor_locator)
            wc = weight_chart.plot(self.feeds_data['weight'].dates,
                                   self.feeds_data['weight'].data, color='C0',
                                   label='Weight (Kg)')
            weight_chart.set_ylabel('Weight (Kg)',
                                    fontsize='9',
                                    color='C0')
            weight_chart.tick_params(axis='y',
                                     colors='C0',
                                     which='both')
            weight_chart.grid(which='major')
            weight_chart.yaxis.grid(which='minor')
            # weight_chart.legend(loc='lower left')

            bmi_chart = weight_chart.twinx()
            bmi_chart.yaxis.set_major_locator(bmi_major_locator)
            bc = bmi_chart.plot(self.feeds_data['bmi'].dates,
                                self.feeds_data['bmi'].data, color='C1',
                                label='BMI')
            bmi_chart.set_ylabel('BMI',
                                 fontsize='9',
                                 color='C1')
            bmi_chart.tick_params(axis='y',
                                  colors='C1')
            # bmi_chart.legend(loc='upper right')

            charts = wc + bc
            labels = [chart.get_label() for chart in charts]

            for ax in fig.axes:
                plt.sca(ax)
                plt.xticks(rotation=45)
                ax.tick_params(direction='out', top='off',
                               labelsize='8')
                ax.spines['top'].set_visible(False)

            fig.legend(charts, labels, bbox_to_anchor=(0.93, 0.97))
            fig.tight_layout()
            fig.savefig(self.filename, dpi=100)

            plt.clf()
        except Exception:
            self.logger.exception("Something went wrong with"
                                  + " {0}.".format(self.filename))
        finally:
            pass


class BPChart(Chart):
    """Class for the BPChart image."""

    def draw_chart(self):
        """Draw the chart image."""
        try:
            self.logger.debug("Drawing chart for {0}.".format(self.filename))
            bp_minor_locator = tckr.MultipleLocator(4)
            fig, bp_chart = plt.subplots(1, figsize=(8, 4.8))
            bp_chart.yaxis.set_minor_locator(bp_minor_locator)
            bp_chart.plot(self.feeds_data['systolic'].dates,
                          self.feeds_data['systolic'].data,
                          label='Systolic', alpha=0.5)
            bp_chart.plot(self.feeds_data['diastolic'].dates,
                          self.feeds_data['diastolic'].data,
                          label='Diastolic', alpha=0.5)
            bp_chart.plot(self.feeds_data['pulse'].dates,
                          self.feeds_data['pulse'].data,
                          label='Pulse', alpha=0.5)
            bp_chart.grid(which='major')
            bp_chart.yaxis.grid(which='minor')
            bp_chart.set_ylabel('Blood Pressure (mmHg)\nPulse (BPM)')
            bp_chart.tick_params(axis='y', which='both')
            bp_chart.legend()

            for ax in fig.axes:
                plt.sca(ax)
                plt.xticks(rotation=45)
                ax.tick_params(direction='out', top='off',
                               labelsize='8')
                ax.spines['top'].set_visible(False)
            fig.tight_layout()
            fig.savefig(self.filename, dpi=100)

            plt.clf()

        except Exception:
            self.logger.exception("Something went wrong with"
                                  + " {0}.".format(self.filename))
        finally:
            pass


class SmallCharts(Chart):
    """Class for the SmallCharts image."""

    def draw_chart(self):
        """Draw the chart image."""
        try:
            self.logger.debug("Drawing chart for {0}.".format(self.filename))
            bmi_major_locator = tckr.MultipleLocator(1)
            fig, (weight_chart,
                  bp_chart) = plt.subplots(2, figsize=(4, 4.8))

            bp_chart.plot(self.feeds_data['systolic'].dates,
                          self.feeds_data['systolic'].data,
                          label='Systolic', alpha=0.5)
            bp_chart.plot(self.feeds_data['diastolic'].dates,
                          self.feeds_data['diastolic'].data,
                          label='Diastolic', alpha=0.5)
            bp_chart.plot(self.feeds_data['pulse'].dates,
                          self.feeds_data['pulse'].data,
                          label='Pulse', alpha=0.5)
            bp_chart.set_ylabel('Blood Pressure (mmHg)\nPulse (BPM)')
            bp_chart.tick_params(axis='y')

            weight_chart.plot(self.feeds_data['weight'].dates,
                              self.feeds_data['weight'].data,
                              color='C0', alpha=0.5)
            weight_chart.set_ylabel('Weight (Kg)',
                                    fontsize='9',
                                    color='C0')
            weight_chart.tick_params(axis='y',
                                     colors='C0')

            bmi_chart = weight_chart.twinx()
            bmi_chart.yaxis.set_major_locator(bmi_major_locator)
            bmi_chart.plot(self.feeds_data['bmi'].dates,
                           self.feeds_data['bmi'].data,
                           color='C1', alpha=0.5)
            bmi_chart.set_ylabel('BMI',
                                 fontsize='9',
                                 color='C1')
            bmi_chart.tick_params(axis='y',
                                  colors='C1')

            for ax in fig.axes:
                plt.sca(ax)
                plt.xticks(rotation=45)
                ax.tick_params(direction='out', top='off',
                               labelsize='8')
                ax.spines['top'].set_visible(False)
            fig.tight_layout()
            fig.savefig(self.filename, dpi=100)

            plt.clf()

        except Exception:
            self.logger.exception("Something went wrong with"
                                  + " {0}.".format(self.filename))
        finally:
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
