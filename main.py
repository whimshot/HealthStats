"""Health Stats app in kivy."""
from Adafruit_IO import Client
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

    screen_text = "Health Stats"
    aio = Client(AIO_KEY)

    def new_digit(self, text):
        """Add a digit or decimal point to the input display."""
        logger.debug('{0} key pressed'.format(text))
        try:
            float("0" + self.inputpad.numscreen.text)
            self.inputpad.numscreen.text = self.inputpad.numscreen.text + text
        except Exception:
            self.inputpad.numscreen.text = text
        finally:
            pass

    def statistic_key(self, btn_text):
        """Handle the statistic keys."""
        btn_id = (btn_text.split('\n')[0]).lower()
        logger.debug('{0} key pressed'.format(btn_id))
        vital_text = self.inputpad.numscreen.text
        try:
            vital_stat = float(vital_text)
            if (btn_id == 'weight'):
                bmi = int(vital_stat/BMI_CONSTANT)
                self.aio.send('bmi', bmi)
                logger.debug('BMI of {0} calculated and sent.'.format(bmi))
            self.aio.send(btn_id, vital_stat)
            logger.debug('{0} updated with {1}'.format(btn_id, vital_stat))
        except (ValueError, OSError) as error:
            logger.debug('Caught: {0}'.format(error))
            self.inputpad.numscreen.text = "Health Stats"
        finally:
            self.inputpad.numscreen.text = "Health Stats"

    def delete_key(self, name):
        """Handle the function keys."""
        logger.debug('{0} key pressed.'.format(name))
        try:
            float(self.inputpad.numscreen.text)
            self.inputpad.numscreen.text = self.inputpad.numscreen.text[:-1]
        except Exception:
            self.inputpad.numscreen.text = "Health Stats"
        finally:
            pass

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
