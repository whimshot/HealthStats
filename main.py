"""Health Stats app in kivy."""
from Adafruit_IO import Client
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from StatsChart import StatsChart
from FileMonkey import FileMonkey
from AdafruitIOKey import AIO_KEY


feeds = ['weight', 'diastolic', 'systolic', 'pulse', 'bmi']
statschart = StatsChart()


class HealthStats(BoxLayout):
    """A simple class for a Health Stats app in kivy."""

    screen_text = "Health Stats"
    aio = Client(AIO_KEY)
    fm = FileMonkey('StatsCharts.png')

    def update(self, dt):
        """Update the display and charts."""
        self.inputpad.numscreen.text = self.screen_text

    def update_chart(self, dt):
        """Reload the chart image if it has changed."""
        if (self.fm.ook()):
            self.statsimage.reload()

    def new_digit(self, text):
        """Add a digit or decimal point to the input display."""
        if (self.screen_text == "Health Stats"):
            self.screen_text = text
        else:
            self.screen_text = self.screen_text + text

    def statistic_key(self, name):
        """Handle the statistic keys."""
        vital_text = self.screen_text
        self.screen_text = "updating . . ."
        try:
            vital_stat = float(vital_text)
            if (name == "weight"):
                bmi = int(vital_stat/3.161284)
                self.aio.send('bmi', bmi)
            self.aio.send(name, vital_stat)
        except ValueError:
            self.screen_text = "Health Stats"
        finally:
            self.screen_text = "Health Stats"

    def delete_key(self, name):
        """Handle the function keys."""
        try:
            if (self.screen_text != "Health Stats"):
                self.screen_text = self.screen_text[:-1]
            elif (self.screen_text == ""):
                self.screen_text = "Health Stats"
        except ValueError:
            self.screen_text = "Health Stats"

    pass


class HealthStatsApp(App):
    """Kivy App Class for Health Stats."""

    def build(self):
        """Build function for Health Stats kivy app."""
        hs = HealthStats()
        Clock.schedule_interval(hs.update, 1.0 / 10.0)
        Clock.schedule_interval(hs.update_chart, 5.0)
        return hs


if __name__ == '__main__':
    HealthStatsApp().run()
