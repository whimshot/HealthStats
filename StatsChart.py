"""StatsChart class."""
from AdaData import AdaData
import matplotlib
from FileMonkey import FileMonkey
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class StatsChart(object):
    """Stats charts object."""

    fm = FileMonkey('weight.png')

    def __init__(self):
        """Make that statschart."""
        self.oldweights = AdaData('weight')
        self.oldsystolics = AdaData('systolic')
        self.olddiasolics = AdaData('diastolic')
        self.oldpulses = AdaData('pulse')

    def draw_chart(self):
        """Make the stats chart image."""
        try:
            weights = AdaData('weight')
            systolics = AdaData('systolic')
            diastolics = AdaData('diastolic')

            weights.get_data()
            systolics.get_data()
            diastolics.get_data()

            # Only rebuild images if the data has changed or if
            # there is no image.
            if ((weights != self.oldweights)
                    or (systolics != self.oldsystolics)
                    or (diastolics != self.olddiasolics)
                    or (self.fm.ook())):

                fig, (weight, bp) = plt.subplots(2, figsize=(5, 6))

                bp.plot(systolics.dates, systolics.data)
                bp.plot(diastolics.dates, diastolics.data)
                bp.set_ylabel('Blood Pressure')

                weight.plot(weights.dates, weights.data)
                weight.set_ylabel('Weight (Kg)')
                weight.set_ylim(120, 150)

                for ax in fig.axes:
                    matplotlib.pyplot.sca(ax)
                    plt.xticks(rotation=45)
                    ax.grid(axis='y', linestyle='-.')

                fig.tight_layout()
                fig.savefig('weight.png', dpi=300)

                plt.clf()

        except ValueError as ve:
            print("somethings not right %s" % str(ve))

        finally:
            self.oldweights = weights
            self.oldsystolics = systolics
            self.olddiasolics = diastolics
