from .ups import UPSInterface

__version_tuple__ = (0, 0, 1)
__version__ = '.'.join(map(str, __version_tuple__))


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
