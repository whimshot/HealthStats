from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from Adafruit_IO import Client
import time
from adafruitiokey import aoi_key


class HealthStats(BoxLayout):
    """A simple class for a Health Stats app in kivy."""

    aio = Client(aoi_key)
    aio_feed = 'weight'
    screen_text = "Health Stats"

    def update(self, dt):
        self.inputpad.numscreen.text = self.screen_text

    def new_digit(self, text):
        """Adds a digit or decimal point to the input display"""

        if (self.screen_text == "Health Stats"):
            self.screen_text = text
        else:
            self.screen_text = self.screen_text + text

    def key_function(self, name):
        """handles the function keys"""

        try:
            vital_stat = float(self.screen_text)

            if  (name == "delete"):
                self.screen_text = self.screen_text[:-1]

            elif (name == "weight"):
                date = time.strftime("%Y-%m-%d %H:%M:%S %z")
                self.screen_text = "Health Stats"
                self.aio.send(name, vital_stat)
                bmi = int(vital_stat/3.161284)
                self.aio.send('bmi', bmi)

            elif (name == "systolic"):
                date = time.strftime("%Y-%m-%d %H:%M:%S %z")
                self.screen_text = "Health Stats"
                self.aio.send(name, vital_stat)

            elif (name == "diastolic"):
                date = time.strftime("%Y-%m-%d %H:%M:%S %z")
                self.screen_text = "Health Stats"
                self.aio.send(name, vital_stat)

            elif (name == "pulse"):
                date = time.strftime("%Y-%m-%d %H:%M:%S %z")
                self.screen_text = "Health Stats"
                self.aio.send(name, vital_stat)

        except ValueError:
            self.screen_text = "Health Stats"

    pass


class HealthStatsApp(App):

    def build(self):
        hs = HealthStats()
        Clock.schedule_interval(hs.update, 1.0 / 10.0)
        return hs


if __name__ == '__main__':
    HealthStatsApp().run()
