"""Get data from io.adafruit.com."""
from __future__ import print_function

import logging
import logging.handlers
import os
from datetime import datetime

import httplib2
from Adafruit_IO import Client, MQTTClient
from apiclient import discovery
from dateutil import tz
from oauth2client import client, tools
from oauth2client.file import Storage

from hsconfig import config
from hslogger import HostnameFilter

AIO_KEY = config.get('Adafruit', 'aio_key')
AIO_ID = config.get('Adafruit', 'aio_id')
SCOPES = config.get('GoogleSheets', 'scopes')
CLIENT_SECRET_FILE = config.get('GoogleSheets', 'client_secret_file')
APPLICATION_NAME = config.get('GoogleSheets', 'application_name')
QUICK_JSON = config.get('GoogleSheets', 'quick_json')
DISCOVERYURL = config.get('GoogleSheets', 'discoveryurl')
SPREADSHEETID = config.get('GoogleSheets', 'spreadsheetid')


class GData(object):
    """Get and store data from Google Sheets."""

    def __init__(self, sheet, **kwargs):
        """Put together weight chart."""
        super().__init__(**kwargs)
        try:
            self.logger = \
                logging.getLogger('HealthStats.'
                                  + self.__class__.__name__)
            self.logger.addFilter(HostnameFilter())
            self.data = []
            self.dates = []
            self.dates_utc = []
            self.sheet = sheet
            self.aio = Client(AIO_KEY)
            self.get_data()
            self.client = MQTTClient(AIO_ID, AIO_KEY)
            self.client.on_connect = self.connected
            self.client.on_disconnect = self.disconnected
            self.client.on_message = self.message
            self.client.connect()
            self.client.loop_background()
            self.logger.debug('Setting up {0} '.format(
                self.__class__.__name__) + 'for {0}.'.format(sheet))
        except Exception:
            self.logger.exception(
                'Failed to instantiate {}.'.format(self.__class__.__name__))
        finally:
            pass

    def get_credentials(self):
        """
        Get valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        try:
            self.quick_json = QUICK_JSON
            self.home_dir = os.path.expanduser('~')
            self.credential_dir = os.path.join(self.home_dir, '.credentials')
            if not os.path.exists(self.credential_dir):
                os.makedirs(self.credential_dir)
            self.credential_path = os.path.join(self.credential_dir,
                                                self.quick_json)
            self.store = Storage(self.credential_path)
            self.credentials = self.store.get()
            if not self.credentials or self.credentials.invalid:
                self.flow = client.flow_from_clientsecrets(
                    CLIENT_SECRET_FILE, SCOPES)
                self.flow.user_agent = APPLICATION_NAME
                self.credentials = tools.run(self.flow, self.store)
                self.logger.info('Storing credentials to ' +
                                 self.credential_path)
            return self.credentials
        except Exception as e:
            raise
        finally:
            pass

    def get_data(self):
        """Show basic usage of the Sheets API.

        Creates a Sheets API service object and prints the names and majors of
        students in a sample spreadsheet:
        https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
        """
        try:
            # from_zone = tz.tzutc()
            # to_zone = tz.tzlocal()
            __old_data = self.data
            self.data = []
            self.data = []
            __data = []
            __dates = []
            self.credentials = self.get_credentials()
            self.http = self.credentials.authorize(httplib2.Http())
            self.discoveryUrl = DISCOVERYURL
            self.service = discovery.build(
                'sheets', 'v4', http=self.http,
                discoveryServiceUrl=self.discoveryUrl)

            self.spreadsheetId = SPREADSHEETID
            self.rangeName = self.sheet + '!A2:B'
            self.result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheetId,
                range=self.rangeName).execute()
            self.values = self.result.get('values', [])

            if not self.values:
                print('No data found.')
            else:
                # print('{0:21} {1:5}'.format('date', 'value'))
                for row in self.values:
                    # utc = datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S UTC')
                    # utc = utc.replace(tzinfo=from_zone)
                    # local = utc.astimezone(to_zone).strftime('%Y/%m/%d %H:%M:%S')
                    # Print columns A and E, which correspond to indices 0 and 4.
                    row_date = datetime.strptime(row[0], '%m/%d/%Y %H:%M:%S')
                    # print('{0:21} {1:5}'.format(row[0], row[1]))
                    __data.append(row[1])
                    __dates.append(row_date)
            self.data = __data
            self.dates = __dates
            if self.data != __old_data:
                self.updated = [True, True, True]
        except Exception as e:
            raise
        finally:
            pass

    def send_data(self, value):
        """
        Send data to google sheets and to Adafruit.

        Why? Because that is how we roll!
        """
        try:
            __now_dt = datetime.now()
            __now_str = __now_dt.strftime('%m/%d/%Y %H:%M:%S')
            values = [[__now_str, value]]
            self.credentials = self.get_credentials()
            self.http = self.credentials.authorize(httplib2.Http())
            self.discoveryUrl = DISCOVERYURL
            self.service = discovery.build('sheets', 'v4', http=self.http,
                                           discoveryServiceUrl=self.discoveryUrl)
            self.spreadsheetId = '19-Q4v0r1TedP50e_hGsZcGFtDSQ6jwXIBRwBG8N3k-w'

            body = {'values': values}
            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheetId, range=self.rangeName,
                valueInputOption='USER_ENTERED', body=body).execute()
            self.aio.send(self.sheet, value)
        except Exception as e:
            raise
        finally:
            pass

    def connected(self, client):
        """Called when connection to io.adafruit.com is successful."""
        # Subscribe to changes for the feeds listed.
        self.logger.debug('Connected to Adafruit.')
        try:
            self.logger.debug('Subscribing to {0} feed.'.format(self.sheet))
            self.client.subscribe(self.sheet)
        except Exception:
            self.logger.exception('Failed to subscribe to feed.')

    def disconnected(self, client):
        """Called when disconnected from io.adafruit.com."""
        self.logger.info('Disconnected from Adafruit IO!')

    def message(self, client, feed_id, payload):
        """Called when a subscribed feed gets new data."""
        try:
            self.logger.debug("Feed: {0} received".format(feed_id)
                              + " new data: {0}".format(payload))
            self.get_data()
        except Exception:
            raise
        finally:
            pass


feed_names = ['bmi', 'weight', 'systolic', 'diastolic', 'pulse']
feeds = {}
for feed in feed_names:
    feeds[feed] = GData(feed)


class AdaFeed(object):
    """AdaData object."""

    def __init__(self, feed):
        """Create new AdaData instance."""
        try:
            self.logger = logging.getLogger('HealthStats.'
                                            + self.__class__.__name__)
            self.logger.addFilter(HostnameFilter())
            self.feed = feed
            self.data = []
            self.dates = []
            self.dates_utc = []
            self.aio = Client(AIO_KEY)
            self.from_zone = tz.tzutc()
            self.to_zone = tz.tzlocal()
            self.client = MQTTClient(AIO_ID, AIO_KEY)
            self.client.on_connect = self.connected
            self.client.on_disconnect = self.disconnected
            self.client.on_message = self.message
            self.client.connect()
            self.logger.debug('Data instance for {0}.'.format(feed))
            self.client.loop_background()
            self.get_data()
        except Exception:
            self.logger.exception('Failed to instantiate AdaFeed.')

    def __eq__(self, other):
        """`Are they the same?` Is the question."""
        self.logger.debug('Comparing two instances of AdaFeed.')
        return self.__dict__ == other.__dict__

    def get_data(self):
        """Get data from io.adatruit.com."""
        try:
            old_data = self.data
            self.logger.debug('Querying {0}.'.format(self.feed))
            self.data = []
            self.dates = []
            self.dates_utc = []
            feed_data = self.aio.data(self.feed)
            self.logger.debug('Parsing dates from {0}'.format(self.feed))
            for entry in feed_data:
                self.data.append(float(entry.value))
                self.dates_utc.append(entry.created_at)
                self.logger.debug('Appended {0}'.format(entry.value))
                utc = datetime.strptime(entry.created_at, '%Y-%m-%dT%H:%M:%SZ')
                utc = utc.replace(tzinfo=self.from_zone)
                local = utc.astimezone(self.to_zone)
                self.dates.append(local)
                self.logger.debug('Appended {0}'.format(local))
            self.logger.debug('Retrieved data from {0}.'.format(self.feed))
            if self.data != old_data:
                self.updated = [True, True, True]
        except Exception:
            self.logger.exception('Caught exception.')

    def connected(self, client):
        """Called when connection to io.adafruit.com is successful."""
        # Subscribe to changes for the feeds listed.
        self.logger.debug('Connected to Adafruit, subscribing to feeds.')
        try:
            self.logger.debug('Subscribing to {0} feed.'.format(self.feed))
            self.client.subscribe(self.feed)
        except Exception:
            self.logger.exception('Failed to subscribe to feed.')

    def disconnected(self, client):
        """Called when disconnected from io.adafruit.com."""
        self.logger.info('Disconnected from Adafruit IO!')

    def message(self, client, feed_id, payload):
        """Called when a subscribed feed gets new data."""
        try:
            self.logger.debug("Feed: {0} received".format(feed_id)
                              + " new data: {0}".format(payload))
            self.get_data()
        except Exception:
            raise
        finally:
            pass


class AdaData():
    """This is where we store the data from all the feeds."""

    def __init__(self):
        """
        Initial AdaData.

        Sets up initial containers for data from io.adafruit.com to
        compare against for changes later.
        """
        try:
            self.feeds = ['weight', 'diastolic', 'systolic', 'pulse', 'bmi']
            self.feeds_data = {}     # The data last retrieved from the feeds.
            self.filename = ""
            self.logger = \
                logging.getLogger('HealthStats.'
                                  + self.__class__.__name__)
            self.logger.addFilter(HostnameFilter())
            self.logger.info('creating an instance of ChartMaker')
            self.client = MQTTClient(AIO_ID, AIO_KEY)
            self.client.on_connect = self.connected
            self.client.on_disconnect = self.disconnected
            self.client.on_message = self.message

            for feed in self.feeds:
                self.feeds_data[feed] = AdaFeed(feed)
                self.logger.debug("Getting data from io.adatfruit.com"
                                  + " for {0}.".format(feed))
                self.feeds_data[feed].get_data()

            self.client.connect()
            self.logger.debug('Getting AdaData instance up and running.')
            self.client.loop_background()
        except Exception:
            self.logger.exception('AdaData instantiation failed.')

    def get_data(self):
        """Retrieve data from io.adafruit.com."""
        try:
            for feed in self.feeds:
                self.feeds_data[feed].get_data()
        except Exception:
            raise
        finally:
            pass

    def connected(self, client):
        """Called when connection to io.adafruit.com is successful."""
        # Subscribe to changes for the feeds listed.
        self.logger.debug('Connected to Adafruit, subscribing to feeds.')
        try:
            for feed in self.feeds:
                self.logger.debug('Subscribing to {0} feed.'.format(feed))
                self.client.subscribe(feed)
        except Exception:
            self.logger.exception('Failed to subscribe to feed.')

    def disconnected(self, client):
        """Called when disconnected from io.adafruit.com."""
        self.logger.info('Disconnected from Adafruit IO!')

    def message(self, client, feed_id, payload):
        """Called when a subscribed feed gets new data."""
        try:
            self.logger.debug("Feed: {0} received".format(feed_id)
                              + " new data: {0}".format(payload))
            self.feeds_data[feed_id].get_data()
            if (feed_id in ('weight', 'bmi')):
                self.weight_chart()
            if (feed_id in ('systolic', 'diastolic', 'pulse')):
                self.bp_chart()
            if (feed_id in ('systolic', 'diastolic', 'pulse',
                            'weight', 'bmi')):
                self.small_charts()
        except Exception:
            raise
        finally:
            pass


if __name__ == '__main__':
    gd = GData('bmi')
    gd.get_data()
    print(gd.data)
    print(len(gd.data))
    data = 23
    gd.send_data(data)
