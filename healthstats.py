"""Health Stats app in kivy."""
import cProfile
import logging
import logging.handlers

import chart  # noqa
import inputpad  # noqa
from hslogger import logger, HostnameFilter
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config, ConfigParser
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from kivy.uix.togglebutton import ToggleButton
import os
cwd = os.getcwd()

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')

feeds = ['weight', 'diastolic', 'systolic', 'pulse', 'bmi']


class TglBtn(ToggleButton):
    """The Carousel to hold our information slides."""

    def __init__(self, **kwargs):
        """Build that Weather Slide."""
        super(TglBtn, self).__init__(**kwargs)
        try:
            self.logger = \
                logging.getLogger('HealthStats.'
                                  + self.__class__.__name__)
            self.logger.addFilter(HostnameFilter())
            self.logger.debug(self.__class__.__name__ + ": Created")
            self.text = 'Scroll Off'
        except Exception:
            self.logger.exception("Caught exception.")
        finally:
            pass

    def toggle(self):
        """Toggle that button."""
        try:
            if self.state == 'normal':
                self.text = 'Scroll Off'
            else:
                self.text = 'Scroll On'
        except Exception:
            raise
        finally:
            pass


class HealthStats(BoxLayout):
    """A simple class for a Health Stats app in kivy."""

    pass


class HealthCarousel(Carousel):
    """A carousel of health, renew, renew, renew."""

    def next_slide_please(self, dt):
        """Go to the next slide in the carousel."""
        try:
            if self.parent.toolbar.toggle.state == 'down':
                self.load_next(mode='next')
        except Exception:
            logger.exception("Failed to load next slide.")
        finally:
            pass

    pass


class HealthBox(BoxLayout):
    """A carousel of health, renew, renew, renew."""

    pass


class HealthStatsApp(App):
    """Kivy App Class for Health Stats."""

    def on_start(self):
        """Task performed on start."""
        self.profile = cProfile.Profile()
        self.profile.enable()

    def on_stop(self):
        """Task performed on app stop."""
        self.profile.disable()
        self.profile.dump_stats('healthstats.profile')

    def build_settings(self, settings):
        """Set up the settings for this app."""
        self.config = ConfigParser()
        self.config.read('healthstats.conf')
        settings.add_json_panel('The Health Statistitics',
                                self.config, 'healthstats.json')

    def build(self):
        """Build function for Health Stats kivy app."""
        logger.info('Starting HealthStatsApp.')
        hb = HealthBox()
        Clock.schedule_interval(hb.hc.weightchart.redraw, 30)
        Clock.schedule_interval(hb.hc.bpchart.redraw, 30)
        Clock.schedule_interval(hb.hc.sw.redraw, 30)
        Clock.schedule_interval(hb.hc.sbp.redraw, 30)
        Clock.schedule_interval(hb.hc.healthstats.statsimage.redraw, 30)
        Clock.schedule_interval(hb.hc.next_slide_please, 10)
        return hb


if __name__ == '__main__':
    HealthStatsApp().run()
