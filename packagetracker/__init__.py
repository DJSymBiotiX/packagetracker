from .ups import UPSInterface

from .version import __VERSION__


class Package(object):

    def __init__(self, ups_config=None):
        self.interfaces = {
            'UPS': UPSInterface(ups_config)
            # 'FedEx': FedexInterface(),
            # 'USPS': USPSInterface()
        }

    def get_interface(self, tracking_number):
        shipper = None
        for shipper_id, iface in self.interfaces.iteritems():
            if iface.identify(tracking_number):
                shipper = shipper_id
                break
        return self.interfaces[shipper]

    def track(self, tracking_number):
        return self.get_interface(tracking_number).track(tracking_number)

    def url(self, tracking_number):
        return self.get_interface(tracking_number).url(tracking_number)

    def validate(self, tracking_number):
        return self.get_interface(tracking_number).validate(tracking_number)
