###############################################################################
# This file is part of openWNS (open Wireless Network Simulator)
# _____________________________________________________________________________
#
# Copyright (C) 2004-2010
# Chair of Communication Networks (ComNets)
# Kopernikusstr. 5, D-52074 Aachen, Germany
# phone: ++49-241-80-27910,
# fax: ++49-241-80-22242
# email: info@openwns.org
# www: http://www.openwns.org
# _____________________________________________________________________________
#
# openWNS is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License version 2 as published by the
# Free Software Foundation;
#
# openWNS is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
# This trick assures we use the dummy parameters in 
# ./openwns/wrowser/simdb/SimConfig when in systemTest. 
import sys
import os
sys.path.insert(0, os.getcwd())

# Main modules needed by openWNS
import openwns
import openwns.eventscheduler
import openwns.node
import openwns.distribution
import openwns.evaluation.default
import openwns.probebus

# Modules needed for the load generator
import constanze.traffic
import constanze.node
import constanze.evaluation.default

# Modules needed by ip (Network Layer simulator module)
import ip.Component
from ip.VirtualARP import VirtualARPServer
from ip.VirtualDHCP import VirtualDHCPServer
from ip.VirtualDNS import VirtualDNSServer
import ip.evaluation.default

# Modules needed by glue (Data Link Layer simulator module)
import Tutorial

# Modules needed by copper (Physical Layer simulator module)
import copper.Copper

# Probe configuration
import Evaluation


from openwns.wrowser.simdb.SimConfig import params

# Main configuration parameters:
class Configuration:

    # Maximum simulation time
    maxSimTime = 10 # seconds

    # Number of stations in the scenario (must be < 250 as otherwise the IP addresses will be out of range)
    numberOfStations = params.nStations

    # Link data rate
    speed = 100E6 # bit/second

    # Fixed PDU size at load generator
    fixedPacketSize = 1500 * 8 # bit

    # Traffic generator will offer traffic with speed * load
    load = params.load

    # Fixed Bit Error Rate
    fixedBER = 1E-5


configuration = Configuration()


# Create an instance of the openWNS configuration
# The variable must be called WNS!!!!
WNS = openwns.Simulator(simulationModel = openwns.node.NodeSimulationModel())
WNS.outputStrategy = openwns.simulator.OutputStrategy.DELETE
WNS.maxSimTime = configuration.maxSimTime


# Create a single "wire" instance all stations will attach to
wire = copper.Copper.Wire("theWire")


throughputPerStation = configuration.speed * configuration.load / configuration.numberOfStations


# Configuration of the protocol stack of a single station
class Station(openwns.node.Node):

    def __init__(self, wire, ber, speed, id, stationType = "client"):
        super(Station, self).__init__("node" + str(id))

        self.contextProviders.append(
            openwns.probebus.ConstantContextProvider(
                "DLL.StationType", Evaluation.toStaTypeId(stationType)))

        # Physical Layer (PHY)
        self.phy = copper.Copper.Transceiver(self,
                                             # Name of the PHY
                                             "phy",

                                             # Medium to which the instance is attached to
                                             wire,

                                             # BER this instance experiences
                                             ber,

                                             # Transmit data rate
                                             speed)

        # Data Link Layer (DLL)
        self.dll = Tutorial.Experiment6(self, "ShortCut", 
                                        self.phy.dataTransmission, self.phy.notification, 
                                        stationType = stationType)

        # Network Layer (NL)
        domainName = "node" + str(id) + ".glue.wns.org"
        self.nl = ip.Component.IPv4Component(self,
                                             # Name of the NL
                                             domainName + ".ip",

                                             # Domain name
                                             domainName)

        # Connect NL instance to the DLL interface
        self.nl.addDLL(
            # Name of the DLL interface (Only used within the NL module. Hence, it may differ from
            # the name given to the DLL instance during instantiation)
            _name = "glue",

            # Where to get my IP Address
            _addressResolver = ip.AddressResolver.VirtualDHCPResolver("theOnlySubnet"),

            # ARP zone
            _arpZone = "theOnlySubnet",

            # We can deliver locally
            _pointToPoint = False,

            # DLL SAP for outgoing unicast transmissions
            _dllDataTransmission = self.dll.unicastDataTransmission,

            # DLL SAP for incoming unicast transmissions
            _dllNotification = self.dll.unicastNotification)


        # Traffic generator
        self.load = constanze.node.ConstanzeComponent(self, "constanze", parentLogger = self.logger)




# Create router station
station = Station(wire, openwns.distribution.Fixed(configuration.fixedBER), configuration.speed, 0, stationType = "router")
WNS.simulationModel.nodes.append(station)

# Create client stations
for i in xrange(1, configuration.numberOfStations):
    station = Station(wire, openwns.distribution.Fixed(configuration.fixedBER), configuration.speed, i, stationType = "client")
    WNS.simulationModel.nodes.append(station)


# Configure the traffic generators and determine the destinations for the generated traffic
class DoubleNegExp(constanze.traffic.Poisson):

    def __init__(self,  offset = 0.0, throughput = 1024, packetSize = 1024, duration = 0.0, parentLogger = None):
        super(DoubleNegExp, self).__init__(offset, throughput, packetSize, duration, parentLogger)
        self.packetSize = openwns.distribution.NegExp(packetSize)


ipListenerBinding = constanze.node.IPListenerBinding(WNS.simulationModel.nodes[0].nl.domainName,
                                                     parentLogger = WNS.simulationModel.nodes[0].logger)
listener = constanze.node.Listener(WNS.simulationModel.nodes[0].nl.domainName + ".listener",
                                   parentLogger = WNS.simulationModel.nodes[0].logger)
WNS.simulationModel.nodes[0].load.addListener(ipListenerBinding, listener)

for i in xrange(1, configuration.numberOfStations):
    dne = DoubleNegExp(0.01, throughputPerStation, configuration.fixedPacketSize,
                                parentLogger = WNS.simulationModel.nodes[0].logger)
    ipBinding = constanze.node.IPBinding(WNS.simulationModel.nodes[0].nl.domainName, WNS.simulationModel.nodes[i].nl.domainName,
                                         parentLogger = WNS.simulationModel.nodes[0].logger)
    WNS.simulationModel.nodes[0].load.addTraffic(ipBinding, dne)

    dne = DoubleNegExp(0.01, throughputPerStation, configuration.fixedPacketSize,
                       parentLogger = WNS.simulationModel.nodes[i].logger)
    ipBinding = constanze.node.IPBinding(WNS.simulationModel.nodes[i].nl.domainName, WNS.simulationModel.nodes[0].nl.domainName,
                                         parentLogger = WNS.simulationModel.nodes[i].logger)
    WNS.simulationModel.nodes[i].load.addTraffic(ipBinding, dne)
    ipListenerBinding = constanze.node.IPListenerBinding(WNS.simulationModel.nodes[i].nl.domainName,
                                                         parentLogger = WNS.simulationModel.nodes[i].logger)
    listener = constanze.node.Listener(WNS.simulationModel.nodes[i].nl.domainName + ".listener",
                                       parentLogger = WNS.simulationModel.nodes[i].logger)
    WNS.simulationModel.nodes[i].load.addListener(ipListenerBinding, listener)


# Setup vitual ARP, DHCP and DNS servers
varp = VirtualARPServer("vARP", "theOnlySubnet")
WNS.simulationModel.nodes = [varp] + WNS.simulationModel.nodes

vdhcp = VirtualDHCPServer("vDHCP@",
                          "theOnlySubnet",
                          "192.168.0.2", "192.168.254.253",
                          "255.255.0.0")
WNS.simulationModel.nodes.append(vdhcp)

vdns = VirtualDNSServer("vDNS", "ip.DEFAULT.GLOBAL")
WNS.simulationModel.nodes.append(vdns)


# Configure probes for evaluation
Evaluation.installEvaluation(sim = WNS,
                             loggingStations = range(1, configuration.numberOfStations + 1),
                             dll = WNS.simulationModel.nodes[1].dll,
                             maxPacketDelay = 0.5,     # s
                             maxPacketSize = 2000*8,   # Bit
                             maxBitThroughput = 10E6,  # Bit/s
                             maxPacketThroughput = 1E6, # Packets/s
                             delayResolution = 1000,
                             sizeResolution = 2000,
                             throughputResolution = 10000)

node = openwns.evaluation.createSourceNode(WNS, "glue.phyTrace") 
node.getLeafs().appendChildren(
    openwns.evaluation.JSONTrace(key="__json__", description="JSON testing in PhyUser"))

#openwns.evaluation.default.installEvaluation(sim = WNS)
openwns.setSimulator(WNS)
