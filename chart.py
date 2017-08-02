"""Health Stats app in kivy."""
import logging
import logging.handlers

import matplotlib
import pandas as pd
from adadata import AdaFeed
from hsconfig import config
from hslogger import HostnameFilter
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from matplotlib.ticker import MultipleLocator  # noqa

matplotlib.use('module://kivy.garden.matplotlib.backend_kivyagg')
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas  # noqa
import matplotlib.pyplot as plt  # noqa

AIO_KEY = config.get('Adafruit', 'aio_key')
AIO_ID = config.get('Adafruit', 'aio_id')

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
            self.logger = \
                logging.getLogger('HealthStats.'
                                  + self.__class__.__name__)
            self.logger.addFilter(HostnameFilter())
            self.logger.debug('Setting up weight chart.')
            self.logger.debug('Set trigger for redrawing.')
            self.draw_chart()
            self.logger.debug('Weight: {0}'.format(weight.updated))
            self.logger.debug('BMI: {0}'.format(bmi.updated))
        except Exception:
            raise
        finally:
            pass

    def redraw(self, dt):
        """Start the clock on redrawing the chart."""
        try:
            if (any(weight.updated)
                    and any(bmi.updated)):
                self.logger.debug('Redrawing: {0}'.format(
                    self.__class__.__name__))
                self.draw_chart()
                weight.updated.pop(0)
                weight.updated.append(False)
                bmi.updated.pop(0)
                bmi.updated.append(False)
            self.logger.debug('Weight: {0}'.format(weight.updated))
            self.logger.debug('BMI: {0}'.format(bmi.updated))
        except Exception:
            self.logger.exception(
                "Failed draw_chart for {0}".format(self.__class__.__name__))
        finally:
            pass

    def draw_chart(self):
        """Draw the chart."""
        try:
            self.logger.debug('Redrawing the weight chart.')
            self.clear_widgets()
            plt.close()
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
            self.logger = \
                logging.getLogger('HealthStats.'
                                  + self.__class__.__name__)
            self.logger.addFilter(HostnameFilter())
            self.logger.debug('Setting up weight chart.')
            self.logger.debug('Set trigger for redrawing.')
            self.draw_chart()
        except Exception:
            raise
        finally:
            pass

    def redraw(self, dt):
        """Start the clock on redrawing the chart."""
        try:
            if (any(systolic.updated)
                and any(diastolic.updated)
                    and any(pulse.updated)):
                self.logger.debug('Redrawing: {0}'.format(
                    self.__class__.__name__))
                self.draw_chart()
                systolic.updated.pop(0)
                systolic.updated.append(False)
                diastolic.updated.pop(0)
                diastolic.updated.append(False)
                pulse.updated.pop(0)
                pulse.updated.append(False)
            self.logger.debug('Systolic: {0}'.format(systolic.updated))
            self.logger.debug('Diastolic: {0}'.format(diastolic.updated))
            self.logger.debug('Pulse: {0}'.format(pulse.updated))
        except Exception:
            self.logger.exception(
                "Failed draw_chart for {0}".format(self.__class__.__name__))
        finally:
            pass

    def draw_chart(self):
        """Draw the chart."""
        try:
            self.logger.debug('Redrawing the BP chart.')
            self.clear_widgets()
            plt.close()
            bp_minor_locator = MultipleLocator(2)
            fig, bp_chart = plt.subplots(1, figsize=(8, 4.8))
            plt.title('Blood Presure (mmHg) & Pulse (BPM) Measurements')
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


class SmoothWeight(BoxLayout):
    """Our basic widget."""

    def __init__(self, **kwargs):
        """Put together weight chart."""
        super(SmoothWeight, self).__init__(**kwargs)
        try:
            self.logger = \
                logging.getLogger('HealthStats.'
                                  + self.__class__.__name__)
            self.logger.addFilter(HostnameFilter())
            self.logger.debug('Setting up weight chart.')
        except Exception:
            raise
        finally:
            pass

    def redraw(self, dt):
        """Start the clock on redrawing the chart."""
        try:
            safe_to_plot = (len(weight.data) == len(bmi.data))
            if (any(weight.updated)
                    and any(bmi.updated)
                    and safe_to_plot):
                self.logger.debug('Redrawing: {0}'.format(
                    self.__class__.__name__))
                self.logger.debug('Weight: {0}'.format(len(weight.data)))
                self.logger.debug('BMI: {0}'.format(len(bmi.data)))
                self.draw_chart()
                weight.updated.pop(0)
                weight.updated.append(False)
                bmi.updated.pop(0)
                bmi.updated.append(False)
            self.logger.debug('Weight: {0}'.format(weight.updated))
            self.logger.debug('BMI: {0}'.format(bmi.updated))
        except Exception:
            self.logger.exception(
                "Failed draw_chart for {0}".format(self.__class__.__name__))
        finally:
            pass

    def draw_chart(self):
        """Draw the chart."""
        try:
            self.logger.debug('Redrawing the Smooth Weight chart.')
            self.clear_widgets()
            ma_dates = pd.to_datetime(weight.dates_utc, utc=True)
            _weights = []
            for _w in weight.data:
                _weights.append(float(_w))
            self.df = pd.DataFrame(
                {'Weight': _weights},
                index=ma_dates)
            self.logger.debug('\n{0}'.format(self.df.values))
            self.logger.debug('\n{0}'.format(self.df.index))
            upsampled = self.df.resample('H').mean()
            interpolated = upsampled.interpolate(method='polynomial', order=3)
            fig, _weight = plt.subplots(1, figsize=(8, 4.8))
            plt.title('Weight and BMI')
            weight_minor_locator = MultipleLocator(.2)
            bmi_major_locator = MultipleLocator(1)
            _weight.yaxis.set_minor_locator(weight_minor_locator)
            wc1 = _weight.plot(weight.dates,
                               weight.data,
                               label='Weight (Kg)')
            wc2 = _weight.plot(interpolated.index,
                               interpolated['Weight'], '-',
                               label='Weight (Kg) Interpolated')
            _weight.grid(which='major')
            _weight.yaxis.grid(which='minor')
            _weight.set_ylabel('Weight')
            _weight.tick_params(axis='y', which='both')

            _bmi = _weight.twinx()
            _bmi.yaxis.set_major_locator(bmi_major_locator)
            bc = _bmi.plot(bmi.dates,
                           bmi.data,
                           'C2', label='BMI')
            _bmi.set_ylabel('BMI',
                            fontsize='9',
                            color='C2')
            _bmi.tick_params(axis='y',
                                  colors='C2')

            charts = wc1 + wc2 + bc
            labels = [chart.get_label() for chart in charts]

            for ax in fig.axes:
                matplotlib.pyplot.sca(ax)
                plt.xticks(rotation=45)
                ax.tick_params(direction='out', top='off',
                               labelsize='8')
                ax.spines['top'].set_visible(False)

            _weight.legend(charts, labels, ncol=2)
            fig.tight_layout()
            canvas = fig.canvas
            canvas.draw()
            self.add_widget(canvas)
        except Exception:
            raise
        finally:
            pass


class SmoothBP(BoxLayout):
    """Our basic widget."""

    def __init__(self, **kwargs):
        """Put together weight chart."""
        super(SmoothBP, self).__init__(**kwargs)
        try:
            self.logger = logging.getLogger('HealthStats.'
                                            + self.__class__.__name__)
            self.logger.addFilter(HostnameFilter())
            self.logger.debug('Setting up BP chart.')
        except Exception:
            raise
        finally:
            pass

    def redraw(self, dt):
        """Start the clock on redrawing the chart."""
        try:
            safe_to_plot = (len(systolic.data) == len(diastolic.data)
                            and len(diastolic.data) == len(pulse.data))
            if (any(systolic.updated)
                and any(diastolic.updated)
                    and any(pulse.updated)
                    and safe_to_plot):
                self.logger.debug('Redrawing: {0}'.format(
                    self.__class__.__name__))
                self.logger.debug('systolic: {0}'.format(len(systolic.data)))
                self.logger.debug('diastolic: {0}'.format(len(diastolic.data)))
                self.logger.debug('pulse: {0}'.format(len(pulse.data)))
                self.draw_chart()
                systolic.updated.pop(0)
                systolic.updated.append(False)
                diastolic.updated.pop(0)
                diastolic.updated.append(False)
                pulse.updated.pop(0)
                pulse.updated.append(False)
            self.logger.debug('Systolic: {0}'.format(systolic.updated))
            self.logger.debug('Diastolic: {0}'.format(diastolic.updated))
            self.logger.debug('Pulse: {0}'.format(pulse.updated))
        except Exception:
            self.logger.exception(
                "Failed draw_chart for {0}".format(self.__class__.__name__))
        finally:
            pass

    def draw_chart(self):
        """Draw the chart."""
        try:
            self.logger.debug('Redrawing the BP chart.')
            self.clear_widgets()
            sys_dates = pd.to_datetime(systolic.dates_utc, utc=True)
            _systolic = []
            for _sys in systolic.data:
                _systolic.append(float(_sys))
            _diastolic = []
            for _dia in diastolic.data:
                _diastolic.append(float(_dia))
            _pulse = []
            for _pls in pulse.data:
                _pulse.append(float(_pls))
            self.logger.debug("Systolic: {0}".format(_systolic))
            self.logger.debug("Diastolic: {0}".format(_diastolic))
            self.logger.debug("Pulse: {0}".format(_pulse))
            self.df = pd.DataFrame(
                {'Systolic': _systolic,
                 'Diastolic': _diastolic,
                 'Pulse': _pulse},
                index=sys_dates)
            self.logger.debug('\n{0}'.format(self.df.values))
            self.logger.debug('\n{0}'.format(self.df.index))
            downsampled = self.df.resample('D').mean()
            ds_interpolated = downsampled.interpolate(
                method='polynomial', order=2)
            upsampled = ds_interpolated.resample('H').mean()
            interpolated = upsampled.interpolate(
                method='polynomial', order=2)
            fig, _bp = plt.subplots(1, figsize=(8, 4.8))
            bp_minor_locator = MultipleLocator(2)
            plt.title('Blood Presure (mmHg) & Pulse (BPM) Measurements')
            _bp.yaxis.set_minor_locator(bp_minor_locator)
            _bp.plot(systolic.dates,
                     systolic.data,
                     label='Systolic')
            _bp.plot(diastolic.dates,
                     diastolic.data,
                     label='Diastolic')
            _bp.plot(pulse.dates,
                     pulse.data,
                     label='Pulse')
            _bp.plot(interpolated.index,
                     interpolated['Systolic'], '-',
                     label='Systolic Interpolated')
            _bp.plot(interpolated.index,
                     interpolated['Diastolic'], '-',
                     label='Diastolic Interpolated')
            _bp.plot(interpolated.index,
                     interpolated['Pulse'], '-',
                     label='Pulse Interpolated')
            _bp.grid(which='major')
            _bp.yaxis.grid(which='minor')
            _bp.set_ylabel('Blood Presure (mmHg)\n&Pulse (BPM)')
            _bp.tick_params(axis='y', which='both')
            _bp.legend(ncol=2)

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
            self.logger = logging.getLogger('HealthStats.'
                                            + self.__class__.__name__)
            self.logger.addFilter(HostnameFilter())
            self.logger.debug('Setting up weight chart.')
            self.logger.debug('Set trigger for redrawing.')
            self.draw_chart()
        except Exception:
            raise
        finally:
            pass

    def redraw(self, dt):
        """Start the clock on redrawing the chart."""
        try:
            safe_to_plot = (len(systolic.data) == len(diastolic.data)
                            and len(diastolic.data) == len(pulse.data)
                            and len(weight.data) == len(bmi.data))
            if (any(systolic.updated)
                and any(diastolic.updated)
                    and any(pulse.updated)
                    and any(weight.updated)
                    and any(bmi.updated)
                    and safe_to_plot):
                self.logger.debug('Redrawing: {0}'.format(
                    self.__class__.__name__))
                self.draw_chart()
                systolic.updated.pop(0)
                systolic.updated.append(False)
                diastolic.updated.pop(0)
                diastolic.updated.append(False)
                pulse.updated.pop(0)
                pulse.updated.append(False)
                weight.updated.pop(0)
                weight.updated.append(False)
                bmi.updated.pop(0)
                bmi.updated.append(False)
            self.logger.debug('Systolic: {0}'.format(systolic.updated))
            self.logger.debug('Diastolic: {0}'.format(diastolic.updated))
            self.logger.debug('Pulse: {0}'.format(pulse.updated))
            self.logger.debug('Weight: {0}'.format(weight.updated))
            self.logger.debug('BMI: {0}'.format(bmi.updated))
        except Exception:
            self.logger.exception(
                "Failed draw_chart for {0}".format(self.__class__.__name__))
        finally:
            pass

    def draw_chart(self):
        """Draw the chart."""
        try:
            self.logger.debug('Redrawing the small charts.')
            self.clear_widgets()
            plt.close()
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


class ChartApp(App):
    """The Apps the thing."""

    def build(self):
        """Build the app."""
        cs = Chartsel()
        cs.wc.redraw()
        cs.bp.redraw()
        cs.sc.redraw()
        cs.sw.redraw()
        cs.sbp.redraw()
        Clock.schedule_interval(cs.next_slide_please, 5.0)
        return cs


if __name__ == '__main__':
    ChartApp().run()
