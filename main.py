"""Health Stats app in kivy."""
from HSConfig import config
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.config import Config
from HSLogger import logger
from StatsChart import StatsChart
from FileMonkey import FileMonkey
import InputPad


Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')

BMI_CONSTANT = config.getfloat('Constants', 'bmi_constant')
AIO_KEY = config.get('Adafruit', 'aio_key')


logger.info('Setting up HealthStatsApp.')
feeds = ['weight', 'diastolic', 'systolic', 'pulse', 'bmi']
statschart = StatsChart()
statschart.draw_chart()


class Chart(Image):
    """The charts that we display."""

    def __init__(self, **kwargs):
        """Chart object instance."""
        super(Chart, self).__init__(**kwargs)

    def build(self):
        """Builder for chart object."""
        try:
            filename = str(self.source)
            logger.debug("BUILD: Building new chart {0}.".format(filename))
            self.fm = FileMonkey(filename)
        except Exception:
            logger.exception("Caught exception.")
        finally:
            pass

    def update(self, dt):
        """Check and reload image if source has changed."""
        try:
            logger.debug("Updating {0}.".format(self.source))
            if (self.fm.ook()):
                filename = str(self.source)
                logger.debug('{0} has changed, reloading'.format(filename))
                self.reload()
        except Exception:
            logger.exception('Caught exception.')
        finally:
            pass


class HealthStats(BoxLayout):
    """A simple class for a Health Stats app in kivy."""

    pass


class HealthCarousel(Carousel):
    """A carousel of health, renew, renew, renew."""


class HealthStatsApp(App):
    """Kivy App Class for Health Stats."""

    def build(self):
        """Build function for Health Stats kivy app."""
        logger.info('Starting HealthStatsApp.')
        hc = HealthCarousel(direction='top', loop=True)
        hc.weightchart.build()
        hc.bpchart.build()
        hc.healthstats.statsimage.build()
        Clock.schedule_interval(hc.weightchart.update, 5.0)
        Clock.schedule_interval(hc.bpchart.update, 5.0)
        Clock.schedule_interval(hc.healthstats.statsimage.update, 5.0)
        return hc


if __name__ == '__main__':
    HealthStatsApp().run()
