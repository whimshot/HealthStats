"""Health Stats app in kivy."""
from Adafruit_IO import Client
from AdafruitIOKey import aoi_key
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from StatsChart import StatsChart
from FileMonkey import FileMonkey


class HealthStats(BoxLayout):
    """A simple class for a Health Stats app in kivy."""

    screen_text = "Health Stats"
    aio = Client(aoi_key)
    fm = FileMonkey('weight.png')
    statschart = StatsChart()
    statschart.draw_chart()

    def update(self, dt):
        """Update the display and charts."""
        self.inputpad.numscreen.text = self.screen_text
        if (self.fm.ook()):
            self.statsimage.reload()

    def update_charts(self):
        """Make the charts."""
        self.statschart.draw_chart()

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
                self.update_charts()

            elif (name == "systolic"):
                self.screen_text = "Health Stats"
                self.aio.send(name, vital_stat)
                self.update_charts()

            elif (name == "diastolic"):
                self.screen_text = "Health Stats"
                self.aio.send(name, vital_stat)
                self.update_charts()

            elif (name == "pulse"):
                self.screen_text = "Health Stats"
                self.aio.send(name, vital_stat)
                self.update_charts()

        except ValueError:
            self.screen_text = "Health Stats"

    pass


class HealthStatsApp(App):
    """Kivy App Class for Health Stats."""

    def build(self):
        """Build function for Health Stats kivy app."""
        hs = HealthStats()
        Clock.schedule_interval(hs.update, 1.0 / 10.0)
        Clock.schedule_interval(hs.update_charts, 600.0)

        return hs


if __name__ == '__main__':
    HealthStatsApp().run()
