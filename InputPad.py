""""An Input Pad."""
import logging
import logging.handlers

from Adafruit_IO import Client
from HSConfig import config
from HSLogger import HostnameFilter, logger
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

AIO_KEY = config.get('Adafruit', 'aio_key')
AIO_ID = config.get('Adafruit', 'aio_id')
BMI_CONSTANT = config.getfloat('Constants', 'bmi_constant')


class Key(Button):
    """Any key on the input pad."""

    def __init__(self, **kwargs):
        """Number Button object instance."""
        super(Key, self).__init__(**kwargs)
        try:
            self.logger = \
                logging.getLogger('HealthStats.' + __name__)
            self.logger.addFilter(HostnameFilter())
            self.logger.info('Creating an instance of Key.')
        except Exception:
            self.logger.exception("Failed to create instance of key.")
        finally:
            pass

    pass


class NumberKey(Key):
    """Keys used by the number pad, digits and decimals."""

    def keypress(self):
        """What to do when pressed."""
        try:
            self.parent.text = self.text
            self.logger.debug("{0} key pressed.".format(self.text))
        except Exception:
            self.logger.exception("Keypress failed.")
        finally:
            pass

    pass


class DeleteKey(Key):
    """Button used by the number pad, delete."""

    pass


class StatisticKey(Key):
    """Keys used by the function pad."""

    pass


class InputDisplay(Label):
    """Display for the input pad."""

    def __init__(self, **kwargs):
        """Number Button object instance."""
        super(InputDisplay, self).__init__(**kwargs)
        try:
            self.logger = \
                logging.getLogger('HealthStats.' + __name__)
            self.logger.addFilter(HostnameFilter())
            self.logger.info('Creating an instance of Key.')
        except Exception:
            self.logger.exception("Failed to create instance of InputDisplay.")
        finally:
            pass

    def add_digit(self, text):
        """Add new digit to display."""
        try:
            float("0" + self.text)
            self.text = self.text + text
            self.logger.debug("Added {0} to {1}".format(text, self.text))
        except Exception:
            self.text = text
            self.logger.debug("Added {0} to {1}".format(text, self.text))
        finally:
            pass

    def delete(self):
        """Remove the right most character from display."""
        try:
            float(self.text)
            self.text = self.text[:-1]
            self.logger.debug("Display now reads {0}.".format(self.text))
        except Exception:
            self.text = "Health Stats"
            self.logger.debug("Display now reads {0}.".format(self.text))
        finally:
            pass

    pass


class FunctionPad(BoxLayout):
    """The buttons for selecting the type of statistic."""

    def __init__(self, **kwargs):
        """Number Button object instance."""
        super(FunctionPad, self).__init__(**kwargs)
        try:
            self.logger = \
                logging.getLogger('HealthStats.' + __name__)
            self.logger.addFilter(HostnameFilter())
            self.aio = Client(AIO_KEY)
            self.logger.debug('Creating an instance of FunctionPad.')
        except Exception:
            self.logger.exception("Failed to create instance of FunctionPad.")
        finally:
            pass

    def send_data(self, btn_text):
        """Handle the statistic keys."""
        try:
            btn_id = (btn_text.split('\n')[0]).lower()
            self.logger.debug('{0} key pressed.'.format(btn_id))
            vital_text = self.parent.numscreen.text
            vital_stat = float(vital_text)
            if (btn_id == 'weight'):
                bmi = int(vital_stat/BMI_CONSTANT)
                self.aio.send('bmi', bmi)
                self.logger.debug("BMI of {0}".format(bmi)
                                  + " calculated and sent.")
            self.aio.send(btn_id, vital_stat)
            self.logger.debug("{0} updated with".format(btn_id)
                              + " {0}".format(vital_text))
        except Exception:
            self.logger.exception("Problem sending data.")
            self.parent.numscreen.text = "Failed Sending"
        finally:
            self.parent.numscreen.text = "Health Stats"

    pass


class NumberPad(GridLayout):
    """The buttons with the numbers, delete and decimal."""

    def __init__(self, **kwargs):
        """Number Button object instance."""
        super(NumberPad, self).__init__(**kwargs)
        try:
            self.logger = \
                logging.getLogger('HealthStats.' + __name__)
            self.logger.addFilter(HostnameFilter())
            self.logger.debug('Creating an instance of NumberPad.')
        except Exception:
            self.logger.exception("Failed to create instance of NumberPad.")
        finally:
            pass

    def numberkey(self):
        """Update display with new text."""
        try:
            self.parent.numscreen.add_digit(self.text)
            self.logger.debug("Got {0} as new text.".format(self.text))
            self.text = ""
        except Exception:
            self.logger.exception("Number keypress failed.")
        finally:
            pass

    def deletekey(self):
        """Remove the right most character from display."""
        try:
            self.parent.numscreen.delete()
            self.logger.debug("Called display delete method.")
        except Exception:
            self.logger.exception("Failed to call display delete method.")
        finally:
            pass

    pass


class InputPad(BoxLayout):
    """Demo for testing charts."""

    pass


class InputPadApp(App):
    """Kivy App Class for ChartDemo."""

    def build(self):
        """Build function for ChartDemo kivy app."""
        logger.info('Starting ChartDemoApp.')
        ip = InputPad()
        return ip


if __name__ == '__main__':
    InputPadApp().run()
