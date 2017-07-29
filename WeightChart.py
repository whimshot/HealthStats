import logging
import logging.handlers
import threading
import time

import matplotlib
from AdaData import AdaData, AdaFeed
from Adafruit_IO import MQTTClient
from FileMonkey import FileMonkey
from HSConfig import config
from HSLogger import HostnameFilter, logger
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')

matplotlib.use('module://kivy.garden.matplotlib.backend_kivyagg')
import matplotlib.pyplot as plt  # noqa
from matplotlib.ticker import MultipleLocator  # noqa
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas  # noqa

AIO_KEY = config.get('Adafruit', 'aio_key')
AIO_ID = config.get('Adafruit', 'aio_id')

matplotlib.rc('lines', linewidth=0.75, markersize=4,
              linestyle='-', marker='.')
matplotlib.rc('grid', linestyle='-.', linewidth=0.5, alpha=0.5)
matplotlib.rc('legend', framealpha=0.5, loc='best')
# Set matplotlib global linewidth
matplotlib.rcParams['axes.linewidth'] = 0.5


feeds = ['weight', 'diastolic', 'systolic', 'pulse', 'bmi']
feeds_data = {}     # The data last retrieved from the feeds.
for feed in feeds:
    feeds_data[feed] = AdaFeed(feed)
    feeds_data[feed].get_data()

weight_feed = AdaFeed('weight')
weight_feed.get_data()
bmi_feed = AdaFeed('bmi')
bmi_feed.get_data()


class WeightChart(BoxLayout):

    def __init__(self, **kwargs):
        """Put together weight chart."""
        super(WeightChart, self).__init__(**kwargs)
        try:
            self.logger = \
                logging.getLogger('HealthStats.'
                                  + self.__class__.__name__)
            self.logger.addFilter(HostnameFilter())
            self.logger.debug("Creating an instance of " + __name__)
            self.client = MQTTClient(AIO_ID, AIO_KEY)
            self.client.on_connect = self.connected
            self.client.on_disconnect = self.disconnected
            self.client.on_message = self.message
            self.client.connect()
            self.client.loop_background()

            fig, weight_chart = plt.subplots(1, figsize=(8, 4.8))
            weight_minor_locator = MultipleLocator(.2)
            bmi_major_locator = MultipleLocator(1)
            weight_chart.yaxis.set_minor_locator(weight_minor_locator)
            wc = weight_chart.plot(feeds_data['weight'].dates,
                                   feeds_data['weight'].data,
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
            bc = bmi_chart.plot(feeds_data['bmi'].dates,
                                feeds_data['bmi'].data,
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
            canvas = fig.canvas
            canvas.draw()

            self.add_widget(canvas)
        except Exception:
            raise

    def connected(self, client):
        """Called when connection to io.adafruit.com is successful."""
        # Subscribe to changes for the feeds listed.
        try:
            self.logger.debug("Connected and subscribing.")
            self.client.subscribe('weight')
            self.client.subscribe('bmi')
            self.logger.debug("Connected and subscribed.")
        except Exception:
            self.logger.exception("Failed to subscribe to feeds.")

    def disconnected(self, client):
        """Called when disconnected from io.adafruit.com."""
        try:
            self.logger.debug("Disconnected.")
        except Exception:
            self.logger.exception("Disconnection failure.")
        finally:
            pass

    def message(self, client, feed_id, payload):
        """Called when a subscribed feed gets new data."""
        try:
            self.logger.debug("Feed has been updated.")
            self.canvas.draw()
            self.logger.debug("Canvas has been drawn.")
        except Exception:
            self.logger.exception("Message failure.")
        finally:
            pass


class BPChart(BoxLayout):

    def __init__(self, **kwargs):
        """Put together weight chart."""
        super(BPChart, self).__init__(**kwargs)
        try:
            self.logger = \
                logging.getLogger('HealthStats.'
                                  + self.__class__.__name__)
            self.logger.addFilter(HostnameFilter())
            self.logger.debug("Creating an instance of " + __name__)
            self.client = MQTTClient(AIO_ID, AIO_KEY)
            self.client.on_connect = self.connected
            self.client.on_disconnect = self.disconnected
            self.client.on_message = self.message
            self.client.connect()
            self.client.loop_background()

            bp_minor_locator = MultipleLocator(2)
            fig, bp_chart = plt.subplots(1, figsize=(8, 4.8))
            bp_chart.yaxis.set_minor_locator(bp_minor_locator)
            bp_chart.plot(feeds_data['systolic'].dates,
                          feeds_data['systolic'].data,
                          label='Systolic')
            bp_chart.plot(feeds_data['diastolic'].dates,
                          feeds_data['diastolic'].data,
                          label='Diastolic')
            bp_chart.plot(feeds_data['pulse'].dates,
                          feeds_data['pulse'].data,
                          label='Pulse')
            bp_chart.grid(which='major')
            bp_chart.yaxis.grid(which='minor')
            bp_chart.set_ylabel('Blood Pressure (mmHg)\nPulse (BPM)')
            bp_chart.tick_params(axis='y', which='both')
            bp_chart.legend(ncol=2)

            for ax in fig.axes:
                matplotlib.pyplot.sca(ax)
                plt.xticks(rotation=45)
                ax.tick_params(direction='out', top='off',
                               labelsize='8')
                ax.spines['top'].set_visible(False)
            fig.tight_layout()
            canvas = fig.canvas
            canvas.draw()

            self.add_widget(canvas)
        except Exception:
            raise

    def connected(self, client):
        """Called when connection to io.adafruit.com is successful."""
        # Subscribe to changes for the feeds listed.
        try:
            self.logger.debug("Connected and subscribing.")
            self.client.subscribe('systolic')
            self.client.subscribe('diastolic')
            self.client.subscribe('pulse')
            self.logger.debug("Connected and subscribed.")
        except Exception:
            self.logger.exception("Failed to subscribe to feeds.")

    def disconnected(self, client):
        """Called when disconnected from io.adafruit.com."""
        try:
            self.logger.debug("Disconnected.")
        except Exception:
            self.logger.exception("Disconnection failure.")
        finally:
            pass

    def message(self, client, feed_id, payload):
        """Called when a subscribed feed gets new data."""
        try:
            self.logger.debug("Feed has been updated.")
            time.sleep(5)
            self.canvas.draw()
            self.logger.debug("Canvas has been drawn.")
        except Exception:
            self.logger.exception("Message failure.")
        finally:
            pass


class WeightChartApp(App):

    def build(self):
        bp = BPChart()
        return bp


if __name__ == '__main__':
    WeightChartApp().run()
