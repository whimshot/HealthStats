"""Health Stats app in kivy."""
from Adafruit_IO import Client
from adafruitiokey import aoi_key
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import os
import healthstat


statschart = healthstat.StatsChart()
statschart.draw_chart()


class FileMonkey(object):
    """A monkey that watches files."""

    def __init__(self, filename):
        """Make that monkey."""
        self._cached_stamp = 0
        self.filename = filename

    def ook(self):
        """Train that monkey."""
        try:
            stamp = os.stat(self.filename).st_mtime
            if stamp != self._cached_stamp:
                self._cached_stamp = stamp
                return True
            else:
                return False
        except ValueError:
            return False


class HealthStats(BoxLayout):
    """A simple class for a Health Stats app in kivy."""

    screen_text = "Health Stats"
    aio = Client(aoi_key)
    fm = FileMonkey('weight.png')

    def update(self, dt):
        """Update the display and charts."""
        self.inputpad.numscreen.text = self.screen_text
        if (self.fm.ook()):
            self.weightchart.reload()

    def update_charts(self, dt):
        """Make the charts."""
        statschart.draw_chart()

    def new_digit(self, text):
        """Add a digit or decimal point to the input display."""
        if (self.screen_text == "Health Stats"):
            self.screen_text = text
        else:
            self.screen_text = self.screen_text + text

    def key_function(self, name):
        """Handle the function keys."""
        try:
            vital_stat = float(self.screen_text)
            if (name == "delete"):
                self.screen_text = self.screen_text[:-1]
            elif (name == "weight"):
                self.screen_text = "Health Stats"
                self.aio.send(name, vital_stat)
                bmi = int(vital_stat/3.161284)
                self.aio.send('bmi', bmi)

            elif (name == "systolic"):
                self.screen_text = "Health Stats"
                self.aio.send(name, vital_stat)

            elif (name == "diastolic"):
                self.screen_text = "Health Stats"
                self.aio.send(name, vital_stat)

            elif (name == "pulse"):
                self.screen_text = "Health Stats"
                self.aio.send(name, vital_stat)

        except ValueError:
            self.screen_text = "Health Stats"

    pass


class HealthStatsApp(App):
    """Kivy App Class for Health Stats."""

    def build(self):
        """Build function for Health Stats kivy app."""
        hs = HealthStats()
        Clock.schedule_interval(hs.update, 1.0 / 10.0)
        Clock.schedule_interval(hs.update_charts, 5.0)

        return hs


if __name__ == '__main__':
    HealthStatsApp().run()
