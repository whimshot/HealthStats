"""Health Stats app in kivy."""
from Adafruit_IO import Client
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import logging
import logging.handlers
from LogFilters import HostnameFilter
from StatsChart import StatsChart
from FileMonkey import FileMonkey
from AdafruitIOKey import AIO_KEY

#
MAXLOGSIZE = 1000000
# create logger
logger = logging.getLogger('HealthStats')
logger.setLevel(logging.DEBUG)
logger.addFilter(HostnameFilter())
# create file handler which logs even debug messages
logger_fh = logging.handlers.RotatingFileHandler('HealthStats.log',
                                                 maxBytes=MAXLOGSIZE,
                                                 backupCount=8)
logger_fh.setLevel(logging.INFO)
# create console handler with a higher log level
logger_ch = logging.StreamHandler()
logger_ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
logger_formatter = logging.Formatter('%(asctime)s'
                                     + ' %(hostname)s'
                                     + ' %(levelname)s'
                                     + ' %(name)s[%(process)d]'
                                     + ' %(message)s')
logger_fh.setFormatter(logger_formatter)
logger_ch.setFormatter(logger_formatter)
# add the handlers to the logger
logger.addHandler(logger_fh)
logger.addHandler(logger_ch)

logger.info('Setting up HealthStatsApp.')
feeds = ['weight', 'diastolic', 'systolic', 'pulse', 'bmi']
statschart = StatsChart()


class HealthStats(BoxLayout):
    """A simple class for a Health Stats app in kivy."""

    screen_text = "Health Stats"
    aio = Client(AIO_KEY)
    fm = FileMonkey('StatsCharts.png')

    def update(self, dt):
        """Update the display and charts."""
        try:
            self.inputpad.numscreen.text = self.screen_text
            logger.debug('Updated the input display.')
        except Exception:
            logger.exception('Failed to update input display.')

    def update_chart(self, dt):
        """Reload the chart image if it has changed."""
        try:
            if (self.fm.ook()):
                logger.debug('Stats chart image has changed, reloading.')
                self.statsimage.reload()
                logger.debug('Stats chart image reloaded.')
        except Exception:
            logger.exception('Failed to update chart.')

    def new_digit(self, text):
        """Add a digit or decimal point to the input display."""
        logger.debug('{0} key pressed'.format(text))
        if (self.screen_text == "Health Stats"):
            self.screen_text = text
        else:
            self.screen_text = self.screen_text + text

    def statistic_key(self, name):
        """Handle the statistic keys."""
        logger.debug('{0} key pressed'.format(name))
        vital_text = self.screen_text
        try:
            vital_stat = float(vital_text)
            if (name == "weight"):
                bmi = int(vital_stat/3.161284)
                self.aio.send('bmi', bmi)
                logger.debug('BMI of {0} calculated and sent.'.format(bmi))
            self.aio.send(name, vital_stat)
            logger.debug('{0} updated with {1}'.format(name, vital_stat))
        except (ValueError, OSError) as error:
            logger.debug('Caught: {0}'.format(error))
            self.screen_text = "Health Stats"
        finally:
            self.screen_text = "Health Stats"

    def delete_key(self, name):
        """Handle the function keys."""
        logger.debug('{0} key pressed.'.format(name))
        try:
            if (self.screen_text != "Health Stats"):
                self.screen_text = self.screen_text[:-1]
            elif (self.screen_text == ''):
                self.screen_text = "Health Stats"
        except Exception:
            self.screen_text = "Health Stats"
            self.logger.exception('Delete key failed.')

    pass


class HealthStatsApp(App):
    """Kivy App Class for Health Stats."""

    def build(self):
        """Build function for Health Stats kivy app."""
        logger.info('Starting HealthStatsApp.')
        hs = HealthStats()
        Clock.schedule_interval(hs.update, 1.0 / 10.0)
        Clock.schedule_interval(hs.update_chart, 5.0)
        return hs


if __name__ == '__main__':
    HealthStatsApp().run()
