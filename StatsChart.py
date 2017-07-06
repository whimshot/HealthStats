"""StatsChart class."""
from AdaData import AdaData
import matplotlib
from FileMonkey import FileMonkey
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class StatsChart(object):
    """Stats charts object."""

    fm = FileMonkey('StatsCharts.png')

    def __init__(self):
        """
        Initial StatsCart.

        Sets up initial containers for data from io.adafruit.com to
        compare against for changes later.
        """
        self.oldweight = AdaData('weight')
        self.oldsystolic = AdaData('systolic')
        self.olddiastolic = AdaData('diastolic')
        self.oldpulse = AdaData('pulse')

    def draw_chart(self):
        """Make the stats chart image."""
        print("New Chart?")
        try:
            weight = AdaData('weight')
            systolic = AdaData('systolic')
            diastolic = AdaData('diastolic')
            pulse = AdaData('pulse')

            weight.get_data()
            systolic.get_data()
            diastolic.get_data()
            pulse.get_data()

            # Only rebuild images if the data has changed or if
            # there is no image.
            if ((weight != self.oldweight)
                    or (systolic != self.oldsystolic)
                    or (diastolic != self.olddiastolic)
                    or (pulse != self.oldpulse)
                    or (self.fm.ook())):

                print("Making new chart.")

                fig, (weight_chart, bp_chart) = plt.subplots(2, figsize=(5, 6))

                bp_chart.plot(systolic.dates, systolic.data)
                bp_chart.plot(diastolic.dates, diastolic.data)
                bp_chart.set_ylabel('Blood Pressure (mmHg)')

                weight_chart.plot(weight.dates, weight.data)
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

        finally:
            self.oldweight = weight
            self.oldsystolic = systolic
            self.olddiastolic = diastolic
            self.oldpulse = pulse
