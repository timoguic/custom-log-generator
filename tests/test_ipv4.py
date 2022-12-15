from providers._ipv4 import IPv4Network


def test_ipv4():
    network = IPv4Network(cidr="192.168.1.0/24")
    assert network.get_ip_address() == "192.168.1.1"


def test_ipv4_excluded():
    network = IPv4Network(cidr="192.168.1.0/24", excluded=["192.168.1.1"])
    assert network.get_ip_address() == "192.168.1.2"
