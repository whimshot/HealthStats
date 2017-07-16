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


class HealthStats(BoxLayout):
    """A simple class for a Health Stats app in kivy."""

    screen_text = "Health Stats"
    aio = Client(AIO_KEY)
    fm = FileMonkey('ChartImage.png')

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

    def statistic_key(self, btn_text):
        """Handle the statistic keys."""
        btn_id = (btn_text.split('\n')[0]).lower()
        logger.debug('{0} key pressed'.format(btn_id))
        vital_text = self.screen_text
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
        hc = Carousel(direction='right', loop=True)
        hs = HealthStats()
        Clock.schedule_interval(hs.update, 1.0 / 10.0)
        Clock.schedule_interval(hs.update_chart, 5.0)
        wc = Image(source='WeightChart.png', keep_ratio=False,
                   allow_stretch=True)
        bpc = Image(source='BPChart.png', keep_ratio=False,
                    allow_stretch=True)
        hc.add_widget(hs)
        hc.add_widget(wc)
        hc.add_widget(bpc)
        return hc


if __name__ == '__main__':
    HealthStatsApp().run()
