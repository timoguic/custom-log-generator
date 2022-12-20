import ipaddress


class IPv4Network:
    """Wrapper class for the ipaddress.IPv4Network class"""

    def __init__(self, cidr, excluded=None):
        self.network = ipaddress.IPv4Network(cidr)
        self.hosts = self.network.hosts()
        if excluded is None:
            excluded = []
        self.excluded = excluded

    def get_ip_address(self):
        """Returns the "next available" IP from the pool"""
        found_ip = False
        while not found_ip:
            ipaddr = str(next(self.hosts))
            if ipaddr not in self.excluded:
                found_ip = True
        return ipaddr
