"""Health Stats app in kivy."""
import Chart        # noqa
import InputPad     # noqa
from ChartMaker import ChartMaker
from HSConfig import config
from HSLogger import logger
from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')

BMI_CONSTANT = config.getfloat('Constants', 'bmi_constant')
AIO_KEY = config.get('Adafruit', 'aio_key')


logger.info('Setting up HealthStatsApp.')
feeds = ['weight', 'diastolic', 'systolic', 'pulse', 'bmi']


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
        cm = ChartMaker()
        cm.weight_chart()
        cm.bp_chart()
        cm.small_charts()
        hc.weightchart.build()
        hc.bpchart.build()
        hc.healthstats.statsimage.build()
        return hc


if __name__ == '__main__':
    HealthStatsApp().run()
