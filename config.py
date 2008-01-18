import wns.WNS
import wns.EventScheduler
import wns.Node
import wns.Distribution
import speetcl.probes

import constanze.Constanze
import constanze.Node

import ip.Component
from ip.VirtualARP import VirtualARPServer
from ip.VirtualDHCP import VirtualDHCPServer
from ip.VirtualDNS import VirtualDNSServer
import ip

import glue.support.Configuration

import copper.Copper


# These are the important configuration parameters:
class Configuration:
    maxSimTime = 10.0
    # must be < 250 (otherwise IPAddress out of range)
    numberOfStations = 2
    # 100 MBit/s
    speed = 100E6
    # 1500 byte
    fixedPacketSize = 1500 * 8
    # traffic generator will offer traffic with speed*load
    load = 0.5
    # fixed Bit Error Rate
    fixedBER = 1E-5
    # resendTimeout of StopAndWait-ARQ (be careful with this one!)
    resendTimeout = 0.01

configuration = Configuration()

# create an instance of the WNS configuration
# The variable must be called WNS!!!!
WNS = wns.WNS.WNS()
WNS.outputStrategy = wns.WNS.OutputStrategy.DELETE
WNS.maxSimTime = configuration.maxSimTime

wire = copper.Copper.Wire("theWire")

throughputPerStation = configuration.speed * configuration.load / configuration.numberOfStations

# specific station for this test with StopAndWait DLL
class Station(wns.Node.Node):
    phy = None
    dll = None
    nl = None
    load = None

    def __init__(self, wire, ber, speed, id):
        super(Station, self).__init__("node"+str(id))

        # Physical Layer
        self.phy = copper.Copper.Transceiver(self, "phy", wire, ber, speed)

        # Data Link Layer
        self.dll = glue.support.Configuration.AcknowledgedModeShortCutComponent(
            self,
            "ShortCut",
            self.phy.dataTransmission,
            self.phy.notification,
            resendTimeout = configuration.resendTimeout)

        # Network Layer
        domainName = "node" + str(id) + ".glue.wns.org"
        self.nl = ip.Component.IPv4Component(self, domainName + ".ip",domainName)
        self.nl.addDLL(_name = "glue",
                       # Where to get my IP Address
                       _addressResolver = ip.AddressResolver.VirtualDHCPResolver("theOnlySubnet"),
                       # ARP zone
                       _arpZone = "theOnlySubnet",
                       # We can deliver locally
                       _pointToPoint = False,
                       # DLL service names
                       _dllDataTransmission = self.dll.unicastDataTransmission,
                       _dllNotification = self.dll.unicastNotification)

        # Traffic Generator
        self.load = constanze.Node.ConstanzeComponent(self, "constanze")

# Create Nodes and components
for i in xrange(configuration.numberOfStations):
    station = Station(wire, wns.Distribution.Fixed(configuration.fixedBER), configuration.speed, i)
    WNS.nodes.append(station)

for i in xrange(configuration.numberOfStations):
    cbr = constanze.Constanze.CBR(0.01, throughputPerStation, configuration.fixedPacketSize)
    ipBinding = constanze.Node.IPBinding(WNS.nodes[i-1].nl.domainName, WNS.nodes[i].nl.domainName)
    WNS.nodes[i-1].load.addTraffic(ipBinding, cbr)
    ipListenerBinding = constanze.Node.IPListenerBinding(WNS.nodes[i-1].nl.domainName)
    listener = constanze.Node.Listener(WNS.nodes[i-1].nl.domainName + ".listener")
    WNS.nodes[i-1].load.addListener(ipListenerBinding, listener)

# one Virtual ARP Zone
varp = VirtualARPServer("vARP", "theOnlySubnet")
WNS.nodes = [varp] + WNS.nodes

vdhcp = VirtualDHCPServer("vDHCP@",
                          "theOnlySubnet",
                          "192.168.0.2", "192.168.254.253",
                          "255.255.0.0")

vdns = VirtualDNSServer("vDNS", "ip.DEFAULT.GLOBAL")
WNS.nodes.append(vdns)

WNS.nodes.append(vdhcp)

# modify probes afterwards
nodeAccessList = speetcl.probes.AccessList.AccessList('wns.node.Node.id')
nodeAccessList.addRange(min = 1, max = configuration.numberOfStations)
WNS.modules.glue.probes = glue.support.Configuration.AcknowledgedModeShortCutComponent.getProbesDict(nodeAccessList)
