###############################################################################
# This file is part of openWNS (open Wireless Network Simulator)
# _____________________________________________________________________________
#
# Copyright (C) 2004-2009
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

from openwns.evaluation import *

def installEvaluation(sim, loggingStations, dll,
                      maxPacketDelay, maxPacketSize, maxBitThroughput, maxPacketThroughput,
                      delayResolution, sizeResolution, throughputResolution, resolution=1000):

    # Constanze probe configuration (load generator)
    sourceName = 'traffic.endToEnd.packet.incoming.size'
    node = openwns.evaluation.createSourceNode(sim, sourceName)
    node.appendChildren(Enumerated(by = 'DLL.StationType',
                                   keys = [1, 2],
                                   names = ['router', 'client'],
                                   format = "DLL.StationType_%s"))
    node.getLeafs().appendChildren(PDF(name = sourceName,
                                       description = 'packet size [Bit]',
                                       minXValue = 0.0,
                                       maxXValue = maxPacketSize,
                                       resolution = sizeResolution))

    sourceName = 'traffic.endToEnd.packet.incoming.delay'
    node = openwns.evaluation.createSourceNode(sim, sourceName)
    node.appendChildren(Enumerated(by = 'DLL.StationType',
                                   keys = [1, 2],
                                   names = ['router', 'client'],
                                   format = "DLL.StationType_%s"))
    node.getLeafs().appendChildren(PDF(name = sourceName,
                                       description = 'end to end packet delay [s]',
                                       minXValue = 0.0,
                                       maxXValue = maxPacketDelay,
                                       resolution = delayResolution))

    sourceName = 'traffic.endToEnd.window.incoming.bitThroughput'
    node = openwns.evaluation.createSourceNode(sim, sourceName)
    node.appendChildren(Enumerated(by = 'DLL.StationType',
                                   keys = [1, 2],
                                   names = ['router', 'client'],
                                   format = "DLL.StationType_%s"))
    node.getLeafs().appendChildren(PDF(name = sourceName,
                                       description = 'average bit rate [Bit/s]',
                                       minXValue = 0.0,
                                       maxXValue = maxBitThroughput,
                                       resolution = throughputResolution))


    # IP probe configuration (NL)
    for dist in ['hop', 'endToEnd']:
        sourceName = 'ip.%s.packet.incoming.delay' % dist
        node = openwns.evaluation.createSourceNode(sim, sourceName )
        node.appendChildren(Enumerated(by = 'DLL.StationType',
                                       keys = [1, 2],
                                       names = ['router', 'client'],
                                       format = "DLL.StationType_%s"))
        node.getLeafs().appendChildren(PDF(name = sourceName,
                                           description = 'Incoming packet delay [s]',
                                           maxXValue = maxPacketDelay,
                                           resolution = resolution,
                                           minXValue = 0.0))

        sourceName = 'ip.%s.packet.outgoing.delay' % dist
        node = openwns.evaluation.createSourceNode(sim, sourceName )
        node.appendChildren(Enumerated(by = 'DLL.StationType',
                                       keys = [1, 2],
                                       names = ['router', 'client'],
                                       format = "DLL.StationType_%s"))
        node.getLeafs().appendChildren(PDF(name = sourceName,
                                           description = 'Outgoing packet delay [s]',
                                           maxXValue = maxPacketDelay,
                                           resolution = resolution,
                                           minXValue = 0.0))

        sourceName = 'ip.%s.packet.incoming.size' % dist
        node = openwns.evaluation.createSourceNode(sim, sourceName )
        node.appendChildren(Enumerated(by = 'DLL.StationType',
                                       keys = [1, 2],
                                       names = ['router', 'client'],
                                       format = "DLL.StationType_%s"))
        node.getLeafs().appendChildren(PDF(name = sourceName,
                                           description = 'Incoming packet size [Bit]',
                                           maxXValue = maxPacketSize,
                                           resolution = resolution,
                                           minXValue = 0.0))

        sourceName = 'ip.%s.packet.outgoing.size' % dist
        node = openwns.evaluation.createSourceNode(sim, sourceName )
        node.appendChildren(Enumerated(by = 'DLL.StationType',
                                       keys = [1, 2],
                                       names = ['router', 'client'],
                                       format = "DLL.StationType_%s"))
        node.getLeafs().appendChildren(PDF(name = sourceName,
                                           description = 'Outgoing packet size [Bit]',
                                           maxXValue = maxPacketSize,
                                           resolution = resolution,
                                           minXValue = 0.0))

        for direction in ['incoming', 'outgoing', 'aggregated']:

            sourceName = 'ip.%s.window.%s.bitThroughput' % (dist, direction)
            node = openwns.evaluation.createSourceNode(sim, sourceName )
            node.appendChildren(Enumerated(by = 'DLL.StationType',
                                           keys = [1, 2],
                                           names = ['router', 'client'],
                                           format = "DLL.StationType_%s"))
            node.getLeafs().appendChildren(PDF(name = sourceName,
                                               description = '%s throughput [Bit/s]' % direction.capitalize(),
                                               maxXValue = maxBitThroughput,
                                               resolution = resolution,
                                               minXValue = 0.0))


    # Glue probe configuration (DLL)
    fuNameList = map(lambda x: x.functionalUnitName, dll.fun.functionalUnit)

    if "unicastBuffer" in fuNameList:
        sourceName = 'glue.unicastBufferLoss'
        node = openwns.evaluation.createSourceNode(sim, sourceName)
        node.appendChildren(Accept(by = 'openwns.node.Node.id', ifIn = loggingStations))
        node.appendChildren(Enumerated(by = 'DLL.StationType',
                                           keys = [1, 2],
                                           names = ['router', 'client'],
                                           format = "DLL.StationType_%s"))
        node.getLeafs().appendChildren(PDF(name = sourceName,
                                           description = 'Loss ratio in unicast buffer',
                                           minXValue = 0.0,
                                           maxXValue = 1.0,
                                           resolution = 1000))

        sourceName = 'glue.unicastBufferSize'
        node = openwns.evaluation.createSourceNode(sim, sourceName)
        node.appendChildren(Accept(by = 'openwns.node.Node.id', ifIn = loggingStations))
        node.appendChildren(Enumerated(by = 'DLL.StationType',
                                           keys = [1, 2],
                                           names = ['router', 'client'],
                                           format = "DLL.StationType_%s"))
        node.getLeafs().appendChildren(PDF(name = sourceName,
                                           description = 'Unicast buffer size',
                                           minXValue = 0.0,
                                           maxXValue = 1.0,
                                           resolution = 20))



    if "crc" in fuNameList:
        sourceName = 'glue.crcLoss'
        node = openwns.evaluation.createSourceNode(sim, sourceName)
        node.appendChildren(Accept(by = 'openwns.node.Node.id', ifIn = loggingStations))
        node.appendChildren(Enumerated(by = 'DLL.StationType',
                                           keys = [1, 2],
                                           names = ['router', 'client'],
                                           format = "DLL.StationType_%s"))
        node.getLeafs().appendChildren(PDF(name = sourceName,
                                           description = 'Loss ratio in CRC',
                                           minXValue = 0.0,
                                           maxXValue = 1.0,
                                           resolution = 1000))


    probePositions = []

    if "topWindowProbe" in fuNameList:
        probePositions.append("top")
    if "arqWindowProbe" in fuNameList:
        probePositions.append("arq")
    if "bottomWindowProbe" in fuNameList:
        probePositions.append("bottom")


    for where in probePositions:
        for direction in [ 'incoming', 'outgoing', 'aggregated' ]:
            for what in [ 'bit' ]:

                sourceName = 'glue.%s.window.%s.%sThroughput' % (where, direction, what)
                node = openwns.evaluation.createSourceNode(sim, sourceName)
                node.appendChildren(Accept(by = 'openwns.node.Node.id', ifIn = loggingStations))
                node.appendChildren(Enumerated(by = 'DLL.StationType',
                                               keys = [1, 2],
                                               names = ['router', 'client'],
                                               format = "DLL.StationType_%s"))
                node.getLeafs().appendChildren(Moments())

    for where in probePositions:

        sourceName = 'glue.%s.packet.incoming.delay' % where
        node = openwns.evaluation.createSourceNode(sim, sourceName)
        node.appendChildren(Accept(by = 'openwns.node.Node.id', ifIn = loggingStations))
        node.appendChildren(Enumerated(by = 'DLL.StationType',
                                           keys = [1, 2],
                                           names = ['router', 'client'],
                                           format = "DLL.StationType_%s"))
        node.getLeafs().appendChildren(PDF(name = sourceName,
                                description = 'Incoming packet delay (%s)' % where,
                                minXValue = 0.0,
                                maxXValue = 0.001,
                                resolution = 1000))

        sourceName = 'glue.%s.packet.outgoing.delay' % where
        node = openwns.evaluation.createSourceNode(sim, sourceName)
        node.appendChildren(Accept(by = 'openwns.node.Node.id', ifIn = loggingStations))
        node.appendChildren(Enumerated(by = 'DLL.StationType',
                                           keys = [1, 2],
                                           names = ['router', 'client'],
                                           format = "DLL.StationType_%s"))
        node.getLeafs().appendChildren(PDF(name = sourceName,
                                description = 'Outgoing packet delay (%s)' % where,
                                minXValue = 0.0,
                                maxXValue = 0.001,
                                resolution = 1000))

        sourceName = 'glue.%s.packet.incoming.size' % where
        node = openwns.evaluation.createSourceNode(sim, sourceName)
        node.appendChildren(Accept(by = 'openwns.node.Node.id', ifIn = loggingStations))
        node.appendChildren(Enumerated(by = 'DLL.StationType',
                                           keys = [1, 2],
                                           names = ['router', 'client'],
                                           format = "DLL.StationType_%s"))
        node.getLeafs().appendChildren(PDF(name = sourceName,
                                description = 'Incoming packet size (%s)' % where,
                                minXValue = 0.0,
                                maxXValue = 15000.0,
                                resolution = 1000))

        sourceName = 'glue.%s.packet.outgoing.size' % where
        node = openwns.evaluation.createSourceNode(sim, sourceName)
        node.appendChildren(Accept(by = 'openwns.node.Node.id', ifIn = loggingStations))
        node.appendChildren(Enumerated(by = 'DLL.StationType',
                                           keys = [1, 2],
                                           names = ['router', 'client'],
                                           format = "DLL.StationType_%s"))
        node.getLeafs().appendChildren(PDF(name = sourceName,
                                description = 'Outgoing packet size (%s)' % where,
                                minXValue = 0.0,
                                maxXValue = 15000.0,
                                resolution = 1000))
