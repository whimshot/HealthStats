""""A smart chart class.

The chart class is an extension of the kivy image class with the ability
to subscribe to data feeds, redraw itself and reload once a new image
has been generated.
"""
import logging
import logging.handlers
import threading
import time

import matplotlib
from AdaData import AdaData
from Adafruit_IO import MQTTClient
from FileMonkey import FileMonkey
from HSConfig import config
from HSLogger import HostnameFilter, logger
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout

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

feeds_data = AdaData()


class ChartMaker():
    """Stats charts object."""

    filename = ""

    def __init__(self):
        """
        Initial ChartMaker.

        Sets up initial containers for data from io.adafruit.com to
        compare against for changes later.
        """
        try:
            self.logger = \
                logging.getLogger('HealthStats.'
                                  + self.__class__.__name__)
            self.logger.addFilter(HostnameFilter())
            self.logger.info('creating an instance of ChartMaker')
        except Exception:
            self.logger.exception('ChartMaker instantiation failed.')

    def small_charts():
        """Make the stats chart image."""
        try:
            fig, (weight_chart, bp_chart) = plt.subplots(2, figsize=(4, 4.8))
            bmi_major_locator = MultipleLocator(1)

            bp_chart.plot(feeds_data['systolic'].dates,
                          feeds_data['systolic'].data,
                          label='Systolic')
            bp_chart.plot(feeds_data['diastolic'].dates,
                          feeds_data['diastolic'].data,
                          label='Diastolic')
            bp_chart.plot(feeds_data['pulse'].dates,
                          feeds_data['pulse'].data,
                          label='Pulse')
            bp_chart.set_ylabel('Blood Pressure (mmHg)\nPulse (BPM)')
            bp_chart.tick_params(axis='y')

            weight_chart.plot(feeds_data['weight'].dates,
                              feeds_data['weight'].data, 'C0')
            weight_chart.set_ylabel('Weight (Kg)',
                                    fontsize='9',
                                    color='C0')
            weight_chart.tick_params(axis='y',
                                     colors='C0')

            bmi_chart = weight_chart.twinx()
            bmi_chart.yaxis.set_major_locator(bmi_major_locator)
            bmi_chart.plot(feeds_data['bmi'].dates,
                           feeds_data['bmi'].data, 'C1')
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
            canvas = fig.canvas
            canvas.draw()
            fig.savefig('SmallCharts.png', dpi=100)
            canvas = fig.canvas
            canvas.draw()
            plt.clf()
            return canvas
        except Exception:
            pass

    def bp_chart():
        """Make the stats chart image."""
        try:
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
            plt.clf()
            return canvas

        except Exception:
            pass

    def weight_chart():
        """Make the stats chart image."""
        try:
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
            plt.clf()
            return canvas
        except Exception:
            # self.logger.exception('Failed to draw new charts.')
            pass


chart_maker = ChartMaker


class Chart(BoxLayout):
    """The basic Chart class we will build off from here."""

    def __init__(self, **kwargs):
        """Chart object instance."""
        super(Chart, self).__init__(**kwargs)
        try:
            self.logger = \
                logging.getLogger('HealthStats.'
                                  + self.__class__.__name__)
            self.logger.addFilter(HostnameFilter())
            self.logger.info("Creating an instance of " + __name__)
            feeds_data.client.on_message = self.message()
        except Exception:
            self.logger.exception('Chart instantiation failed.')
        finally:
            pass

    def message(self):
        """Called when a subscribed feed gets new data."""
        try:
            # self.logger.debug("Feed: {0} received".format(feed_id)
            #                   + " new data: {0}".format(payload))
            # feeds_data[feed_id].get_data()
            self.canvas.draw
        except Exception:
            raise
        finally:
            pass


class WeightChart(Chart):
    """Class for the WeightChart image."""

    canvas = chart_maker.weight_chart()

    pass


class BPChart(Chart):
    """Class for the BPChart image."""

    canvas = chart_maker.bp_chart()

    pass


class SmallCharts(Chart):
    """Class for the SmallCharts image."""

    canvas = chart_maker.small_charts()

    pass


class ChartDemo(BoxLayout):
    """Demo for testing charts."""


class ChartApp(App):
    """Kivy App Class for ChartDemo."""

    def build(self):
        """Build function for ChartDemo kivy app."""
        logger.info('Starting ChartDemoApp.')
        cd = ChartDemo()
        return cd


if __name__ == '__main__':
    ChartApp().run()
