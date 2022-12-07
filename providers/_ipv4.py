import ipaddress


class IPv4Network:
    def __init__(self, cidr, excluded=None):
        self.network = ipaddress.IPv4Network(cidr)
        self.hosts = self.network.hosts()
        if excluded is None:
            excluded = []
        self.excluded = excluded

    def get_ip_address(self):
        found_ip = False
        while not found_ip:
            ipaddr = str(next(self.hosts))
            if ipaddr not in self.excluded:
                found_ip = True
        return ipaddr
