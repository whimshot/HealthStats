"""HealthStat and StatsChart Classes."""
from adafruitiokey import aoi_key
from datetime import datetime
from Adafruit_IO import Client
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class HealthStat:
    """HealthStats object."""

    aio = Client(aoi_key)

    def __init__(self, feed):
        """Create new HealthStats object."""
        self.feed = feed
        self.data = []
        self.dates = []

    def __eq__(self, other):
        """`Are they the same?` Is the question."""
        return self.__dict__ == other.__dict__

    def get_data(self):
        """Get data from io.adatruit.com."""
        feed_data = self.aio.data(self.feed)
        for entry in feed_data:
            self.data.append(entry.value)
            date = str(entry.created_at).replace('Z', '+0000')
            self.dates.append(datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z"))


class StatsChart:
    """Stats charts object."""

    def __init__(self):
        """Make that statschart."""
        self.oldweights = HealthStat('weight')
        self.systolics = HealthStat('systolic')
        self.diastolics = HealthStat('diastolic')

    def draw_chart(self):
        """Make the stats chart image."""
        try:
            weights = HealthStat('weight')
            systolics = HealthStat('systolic')
            diastolics = HealthStat('diastolic')

            weights.get_data()
            systolics.get_data()
            diastolics.get_data()

            if ((weights != self.oldweights)
                    or (systolics != self.oldsystolics)
                    or (diastolics != self.olddiasolics)):

                fig, (weight, bp) = plt.subplots(2, figsize=(4, 5.5))

                bp.plot(systolics.dates, systolics.data, 'bo')
                bp.plot(diastolics.dates, diastolics.data, 'go')
                bp.set_ylabel('Blood Pressure')

                weight.plot(weights.dates, weights.data)
                weight.set_ylabel('Weight (Kg)')
                weight.set_ylim(120, 150)

                for ax in fig.axes:
                    matplotlib.pyplot.sca(ax)
                    plt.xticks(rotation=45)

                fig.tight_layout()
                fig.savefig('weight.png', dpi=300)

                plt.clf()

        except ValueError as ve:
            print("somethings not right %s" % str(ve))

        finally:
            self.oldweights = weights
            self.oldsystolics = systolics
            self.olddiasolics = diastolics
