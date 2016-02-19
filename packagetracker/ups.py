import urllib
from os.path import expanduser
from datetime import datetime
from ConfigParser import ConfigParser

from .xml_dict import dict_to_xml, xml_to_dict
from .data import TrackingInfo


class UPSInterface(object):
    api_url = 'https://wwwcie.ups.com/ups.app/xml/Track'

    def __init__(self, config=None):
        if config is None:
            self.config_path = expanduser("~/.packagetracker")
        else:
            self.config_path = config

        self.config = ConfigParser()
        self.config.read(self.config_path)
        self.license = None
        self.user_id = None
        self.password = None

        self.attrs = {'xml:lang': 'en-US'}

    def identify(self, tracking_number):
        return tracking_number.startswith('1Z')

    def _read_config_(self):
        try:
            self.license = self.config.get('UPS', 'license_number')
            self.user_id = self.config.get('UPS', 'user_id')
            self.password = self.config.get('UPS', 'password')
        except Exception as e:
            print 'Error[UPS Config File]: %s' % e
            return False
        return True

    def build_access_request(self):
        request = {
            'AccessRequest': {
                'AccessLicenseNumber': self.license,
                'UserId': self.user_id,
                'Password': self.password
            }
        }
        return dict_to_xml(request, self.attrs)

    def build_track_request(self, tracking_number):
        request = {
            'TrackRequest': {
                'Request': {
                    'TransactionReference': {
                        'RequestAction': 'Track'
                    }
                },
                'TrackingNumber': tracking_number
            }
        }
        return dict_to_xml(request)

    def build_request(self, tracking_number):
        return (
            self.build_access_request() +
            self.build_track_request(tracking_number)
        )

    def send_request(self, tracking_number):
        body = self.build_request(tracking_number)
        webf = urllib.urlopen(self.api_url, body)
        resp = webf.read()
        webf.close()
        return resp

    def parse_response(self, raw):
        root = xml_to_dict(raw)['TrackResponse']

        # Check status code?
        # response = root['Response']
        # status_code = response['ResponseStatusCode']
        # description = response['ResponseStatusDescription']

        # Parse delivery date, status, and last_update
        shipment = root['Shipment']
        if 'ScheduledDeliveryDate' in shipment:
            est_delivery_date = datetime.strptime(
                shipment['ScheduledDeliveryDate'], "%Y%m%d"
            )
        else:
            ddu = shipment['DeliveryDateUnavailable']
            est_delivery_date = ddu['Description']

        package = shipment['Package']
        activity = package['Activity']
        last_update_date = datetime.strptime(activity['Date'], "%Y%m%d").date()
        last_update_time = datetime.strptime(activity['Time'], "%H%M%S").time()
        last_update = datetime.combine(last_update_date, last_update_time)
        status = activity['Status']['StatusType']['Description']

        return TrackingInfo(est_delivery_date, status, last_update)

    def track(self, tracking_number):
        "Track a UPS package by number. Returns just a delivery date."
        if self._read_config_():
            resp = self.send_request(tracking_number)
            return self.parse_response(resp)
        else:
            return {}

    def url(self, tracking_number):
        "Return a tracking info detailed URL by number."
        return (
            'http://wwwapps.ups.com/WebTracking/processInputRequest?'
            'TypeOfInquiryNumber=T&InquiryNumber1=%s'
        ) % (tracking_number)

    def validate(self, tracking_number):
        "Return True if this is a valid UPS tracking number."
        tracking_num = tracking_number[2:-1]
        odd_total = 0
        even_total = 0

        for ii, digit in enumerate(tracking_num.upper()):
            try:
                value = int(digit)
            except ValueError:
                value = int((ord(digit) - 63) % 10)

            if (ii + 1) % 2:
                odd_total += value
            else:
                even_total += value

        total = odd_total + even_total * 2
        check = ((total - (total % 10) + 10) - total) % 10
        return (check == int(tracking_number[-1:]))
