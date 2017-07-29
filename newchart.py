"""Health Stats app in kivy."""
from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.carousel import Carousel
from kivy.uix.image import Image

from AdaData import AdaFeed

import matplotlib

matplotlib.use('module://kivy.garden.matplotlib.backend_kivyagg')
import matplotlib.pyplot as plt  # noqa
from matplotlib.ticker import MultipleLocator   # noqa
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas  # noqa

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
matplotlib.rc('lines', linewidth=0.75, markersize=4,
              linestyle='-', marker='.')
matplotlib.rc('grid', linestyle='-.', linewidth=0.5, alpha=0.5)
matplotlib.rc('legend', framealpha=0.5, loc='best')

matplotlib.rcParams['axes.linewidth'] = 0.5

bmi = AdaFeed('bmi')
weight = AdaFeed('weight')
systolic = AdaFeed('systolic')
diastolic = AdaFeed('diastolic')
pulse = AdaFeed('pulse')


class WeightChart(BoxLayout):
    """Our basic widget."""

    def __init__(self, **kwargs):
        """Put together weight chart."""
        super(WeightChart, self).__init__(**kwargs)
        try:
            pass
        except Exception:
            raise
        finally:
            pass

    def draw_chart(self):
        """Draw the chart."""
        try:
            bmi.get_data()
            weight.get_data()
            fig, weight_chart = plt.subplots(1, figsize=(8, 4.8))
            plt.title('Weight and BMI')
            weight_minor_locator = MultipleLocator(.2)
            bmi_major_locator = MultipleLocator(1)
            weight_chart.yaxis.set_minor_locator(weight_minor_locator)
            wc = weight_chart.plot(weight.dates,
                                   weight.data,
                                   'C0', label='Weight (Kg)')
            weight_chart.set_ylabel('Weight (Kg)',
                                    fontsize='9',
                                    color='C0')
            weight_chart.tick_params(axis='y',
                                     colors='C0',
                                     which='both')
            weight_chart.grid(which='major')
            weight_chart.yaxis.grid(which='minor')
            for ax in fig.axes:
                matplotlib.pyplot.sca(ax)
                plt.xticks(rotation=45)
                ax.tick_params(direction='out', top='off',
                               labelsize='8')
                ax.spines['top'].set_visible(False)

            bmi_chart = weight_chart.twinx()
            bmi_chart.yaxis.set_major_locator(bmi_major_locator)
            bc = bmi_chart.plot(bmi.dates,
                                bmi.data,
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
        finally:
            pass


class BPChart(BoxLayout):
    """Our basic widget."""

    def __init__(self, **kwargs):
        """Put together weight chart."""
        super(BPChart, self).__init__(**kwargs)
        try:
            pass
        except Exception:
            raise
        finally:
            pass

    def draw_chart(self):
        """Draw the chart."""
        try:
            systolic.get_data()
            diastolic.get_data()
            pulse.get_data()
            bp_minor_locator = MultipleLocator(2)
            fig, bp_chart = plt.subplots(1, figsize=(8, 4.8))
            plt.title('Blood Pressure and Pulse')
            bp_chart.yaxis.set_minor_locator(bp_minor_locator)
            bp_chart.plot(systolic.dates,
                          systolic.data,
                          label='Systolic')
            bp_chart.plot(diastolic.dates,
                          diastolic.data,
                          label='Diastolic')
            bp_chart.plot(pulse.dates,
                          pulse.data,
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
        finally:
            pass


class SmallCharts(BoxLayout):
    """Our basic widget."""

    def __init__(self, **kwargs):
        """Put together weight chart."""
        super(SmallCharts, self).__init__(**kwargs)
        try:
            pass
        except Exception:
            raise
        finally:
            pass

    def draw_chart(self):
        """Draw the chart."""
        try:
            bmi.get_data()
            weight.get_data()
            systolic.get_data()
            diastolic.get_data()
            pulse.get_data()
            fig, (weight_chart, bp_chart) = plt.subplots(2, figsize=(4, 4.8))
            bmi_major_locator = MultipleLocator(1)

            bp_chart.plot(systolic.dates,
                          systolic.data,
                          label='Systolic')
            bp_chart.plot(diastolic.dates,
                          diastolic.data,
                          label='Diastolic')
            bp_chart.plot(pulse.dates,
                          pulse.data,
                          label='Pulse')
            bp_chart.set_ylabel('Blood Pressure (mmHg)\nPulse (BPM)')
            bp_chart.tick_params(axis='y')

            weight_chart.plot(weight.dates,
                              weight.data, 'C0')
            weight_chart.set_ylabel('Weight (Kg)',
                                    fontsize='9',
                                    color='C0')
            weight_chart.tick_params(axis='y',
                                     colors='C0')

            bmi_chart = weight_chart.twinx()
            bmi_chart.yaxis.set_major_locator(bmi_major_locator)
            bmi_chart.plot(bmi.dates,
                           bmi.data, 'C1')
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
            self.add_widget(canvas)
        except Exception:
            raise
        finally:
            pass


class Chartsel(Carousel):
    """Our basic widget."""

    def __init__(self, **kwargs):
        """Put together weight chart."""
        super(Chartsel, self).__init__(**kwargs)
        try:
            pass
        except Exception:
            raise
        finally:
            pass

    def next_slide_please(self, dt):
        """Go to the next slide in the carousel."""
        try:
            self.load_next(mode='next')
        except Exception:
            pass
        finally:
            pass


class NewChartApp(App):
    """The Apps the thing."""

    def build(self):
        """Build the app."""
        cs = Chartsel()
        cs.wc.draw_chart()
        cs.bp.draw_chart()
        cs.sc.draw_chart()
        Clock.schedule_interval(cs.next_slide_please, 5.0)
        return cs


if __name__ == '__main__':
    NewChartApp().run()
