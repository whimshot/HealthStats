"""StatsChart class."""
from AdaData import AdaData
from AdafruitIOKey import AIO_KEY, AIO_ID
import matplotlib
from Adafruit_IO import MQTTClient
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class StatsChart(object):
    """Stats charts object."""

    feeds = ['weight', 'diastolic', 'systolic', 'pulse', 'bmi']

    def __init__(self):
        """
        Initial StatsCart.

        Sets up initial containers for data from io.adafruit.com to
        compare against for changes later.
        """

        self.client = MQTTClient(AIO_ID, AIO_KEY)
        self.client.on_connect = self.connected
        self.client.on_disconnect = self.disconnected
        self.client.on_message = self.message
        self.client.connect()

        self.weight = AdaData('weight')
        self.systolic = AdaData('systolic')
        self.diastolic = AdaData('diastolic')
        self.pulse = AdaData('pulse')

        self.client.loop_background()
        self.draw_chart()

    def connected(self, client):
        """Called when connection to io.adafruit.com is successful."""
        # Subscribe to changes for the feeds listed.
        for feed in self.feeds:
            self.client.subscribe(feed)

    def disconnected(self, client):
        """Called when disconnected from io.adafruit.com."""
        print('Disconnected from Adafruit IO!')

    def message(self, client, feed_id, payload):
        """Called when a subscribed feed gets new data."""
        self.draw_chart()

    def draw_chart(self):
        """Make the stats chart image."""
        try:
            self.weight.get_data()
            self.systolic.get_data()
            self.diastolic.get_data()
            self.pulse.get_data()

            fig, (weight_chart, bp_chart) = plt.subplots(2, figsize=(5, 6))

            bp_chart.plot(self.systolic.dates, self.systolic.data, 'o-')
            bp_chart.plot(self.diastolic.dates, self.diastolic.data, 'o-')
            bp_chart.set_ylabel('Blood Pressure (mmHg)')

            weight_chart.plot(self.weight.dates, self.weight.data, 'go-')
            weight_chart.set_ylabel('Weight (Kg)')
            weight_chart.set_ylim(120, 150)

            for ax in fig.axes:
                matplotlib.pyplot.sca(ax)
                plt.xticks(rotation=45)
                ax.grid(axis='y', linestyle='-.')

            fig.tight_layout()
            fig.savefig('StatsCharts.png', dpi=300)

            plt.clf()

        except ValueError as ve:
            print("somethings not right %s" % str(ve))

    def run(self):
        self.client.loop_background()
        self.draw_chart()
