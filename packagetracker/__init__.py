from .ups import UPSInterface

from .version import __VERSION__


class Package(object):

    def __init__(self, ups_config=None):
        self.interfaces = {
            'UPS': UPSInterface(ups_config)
            # 'FedEx': FedexInterface(),
            # 'USPS': USPSInterface()
        }

    def track(self, tracking_number):
        shipper = None
        for shipper_id, iface in self.interfaces.iteritems():
            if iface.identify(tracking_number):
                shipper = shipper_id
                break
        return self.interfaces[shipper].track(tracking_number)
