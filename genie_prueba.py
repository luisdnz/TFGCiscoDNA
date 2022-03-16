from genie.conf import Genie
from genie.conf.base import Interface

testbed = Genie.init("testbed2.yaml")

dist_rtr01 = testbed.devices["r1"]
dist_rtr01.connect()

new_loopback = Interface(device = dist_rtr01, name="Loopback12")
new_loopback.ipv4 = "10.255.255.2"
new_loopback.ipv4.netmask = "255.255.255.255"
new_loopback.description = "Created with pyATS and Objects"
new_loopback.shutdown = False



new_loopback.build_config(apply=True)
dist_rtr01.disconnect()
