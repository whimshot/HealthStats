# Health Stats

A little Kivy/Python program for recording basic health statistics (weight, bp, and pulse). The statistics are stored on [Adafruit IO](https://io.adafruit.com/). Right now it is designed to run on a [Raspberry Pi](https://www.raspberrypi.org/) with a [Raspbery Pi Touch Display](https://www.raspberrypi.org/products/raspberry-pi-touch-display/).

## Getting Started

If you are really interested feel free to download and take a look. The requirements file is for Python 2.7 & 3.

### Prerequisites

You'll need Python, Kivy, and some Python modules.

-   adafruit-io version 1.1.0
-   certifi version 2017.4.17
-   chardet version 3.0.4
-   cycler version 0.10.0
-   Cython version 0.25.2
-   docutils version 0.13.1
-   idna version 2.5
-   Kivy version 1.10.0
-   Kivy-Garden version 0.1.4
-   matplotlib version 2.0.2
-   numpy version 1.13.0
-   Pygments version 2.2.0
-   pyparsing version 2.2.0
-   python-dateutil version 2.6.0
-   pytz version 2017.2
-   requests version 2.18.1
-   six version 1.10.0
-   urllib3 version 1.21.1

```
pip install --upgrade -r requirements.txt
```

### Installing

You'll need to create a file to store your Adafruit ID and KEY in, it should look something like this:

_AdafruitIOKey.py_:

```
AIO_KEY = 'Your key goes here.'
AIO_ID = 'Your user id goes here.'
```

#### Installation on Raspberry Pi

At the moment the latest version of [Kivy](https://kivy.org/) takes some work to run on a [Raspberry Pi](https://www.raspberrypi.org/). So if you are going to run this on a [Raspberry Pi](https://www.raspberrypi.org/) you should use the instructions on the [Kivy](https://kivy.org/) web site and read the _[Installation on Rasperry Pi](https://kivy.org/docs/installation/installation-rpi.html)_ page.

## Running the tests

Right now there aren't any tests.

### Break down into end to end tests

### And coding style tests

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

-   [Kivy](https://kivy.org/) - UI Library
-   [Pyton](https://www.python.org/) - Programming Language
-   [atom.io](https://atom.io/) - Editor
-   [Matplotlib](https://matplotlib.org/) - Python 2D Plotting Library

## Contributing

Ya can't.

## Versioning

git

## Authors

-   **Colin Johnson** - _Initial work_ - [WhimShot](https://github.com/WhimShot)

## License

It's Mine! All Mine! Ha Ha Ha Ha!

## Acknowledgments
