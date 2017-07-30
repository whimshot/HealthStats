"""Health Stats app in kivy."""
import chart        # noqa
import inputpad     # noqa
from hslogger import logger
from kivy.app import App
from kivy.config import Config
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')

logger.info('Setting up HealthStatsApp.')
feeds = ['weight', 'diastolic', 'systolic', 'pulse', 'bmi']


class HealthStats(BoxLayout):
    """A simple class for a Health Stats app in kivy."""

    pass


class HealthCarousel(Carousel):
    """A carousel of health, renew, renew, renew."""

    pass


class HealthBox(BoxLayout):
    """A carousel of health, renew, renew, renew."""

    pass


class HealthStatsApp(App):
    """Kivy App Class for Health Stats."""

    def build(self):
        """Build function for Health Stats kivy app."""
        logger.info('Starting HealthStatsApp.')
        hb = HealthBox()
        hb.hc.direction = 'top'
        hb.hc.loop = True
        Clock.schedule_interval(hb.hc.weightchart.redraw, 15)
        Clock.schedule_interval(hb.hc.bpchart.redraw, 15)
        Clock.schedule_interval(hb.hc.healthstats.statsimage.redraw, 15)
        return hb


if __name__ == '__main__':
    HealthStatsApp().run()
