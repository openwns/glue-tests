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

import openwns.module
import openwns.pyconfig
import openwns.node
import openwns.Buffer
import openwns.ARQ
import openwns.CRC
import openwns.Probe
import openwns.FUN
import openwns.logger
import openwns.SAR
import openwns.Tools
import openwns.Multiplexer
import openwns.Group
import openwns.FlowSeparator

import glue.Glue
import glue.Trigger
import glue.Routing
import glue.BERMeasurementReporting
import glue.KeyBuilder


# begin example "glue.fun.tutorial.experiment1"
class Experiment1(glue.Glue.Component2Copper):

    def __init__(self, node, name, phyDataTransmission, phyNotification, **kw):
        super(Experiment1, self).__init__(node, name, phyDataTransmission, phyNotification, **kw)

        self.fun.connect(self.unicastUpperConvergence, self.lowerConvergence)
# end example



# begin example "glue.fun.tutorial.experiment2"
class Experiment2(glue.Glue.Component2Copper):

    def __init__(self, node, name, phyDataTransmission, phyNotification, **kw):
        super(Experiment2, self).__init__(node, name, phyDataTransmission, phyNotification, **kw)

        aloha = openwns.FUN.Node("aloha", glue.Glue.Aloha(commandName = "aloha",
                                                          maximumWaitingTime = 0.01,
                                                          parentLogger = self.logger))

        self.fun.add(aloha)

        self.fun.connect(self.unicastUpperConvergence, aloha)
        self.fun.connect(aloha, self.lowerConvergence)
# end example



# begin example "glue.fun.tutorial.experiment3"
class Experiment3(glue.Glue.Component2Copper):

    def __init__(self, node, name, phyDataTransmission, phyNotification, **kw):
        super(Experiment3, self).__init__(node, name, phyDataTransmission, phyNotification, **kw)

        aloha = openwns.FUN.Node("aloha",
                                 glue.Glue.Aloha(commandName = "aloha",
                                                 maximumWaitingTime = 0.01,
                                                 parentLogger = self.logger))

        crc = openwns.FUN.Node("crc",
                               openwns.CRC.CRC("lowerConvergence",
                                               lossRatioProbeName = 'glue.crcLoss',
                                               parentLogger = self.logger))


        self.fun.add(aloha)
        self.fun.add(crc)

        self.fun.connect(self.unicastUpperConvergence, aloha)
        self.fun.connect(aloha, crc)
        self.fun.connect(crc, self.lowerConvergence)
# end example



# begin example "glue.fun.tutorial.experiment4"
class Experiment4(glue.Glue.Component2Copper):

    def __init__(self, node, name, phyDataTransmission, phyNotification, **kw):
        super(Experiment4, self).__init__(node, name, phyDataTransmission, phyNotification, **kw)

        buffer = openwns.FUN.Node("unicastBuffer",
                                  openwns.Buffer.Dropping(size = 100,
                                                          lossRatioProbeName = 'glue.unicastBufferLoss',
                                                          sizeProbeName = 'glue.unicastBufferSize',
                                                          parentLogger = self.logger))

        aloha = openwns.FUN.Node("aloha",
                                 glue.Glue.Aloha(commandName = "aloha",
                                                 maximumWaitingTime = 0.01,
                                                 parentLogger = self.logger))

        crc = openwns.FUN.Node("crc",
                               openwns.CRC.CRC("lowerConvergence",
                                               lossRatioProbeName = 'glue.crcLoss',
                                               parentLogger = self.logger))


        self.fun.add(buffer)
        self.fun.add(aloha)
        self.fun.add(crc)

        self.fun.connect(self.unicastUpperConvergence, buffer)
        self.fun.connect(buffer, aloha)
        self.fun.connect(aloha, crc)
        self.fun.connect(crc, self.lowerConvergence)
# end example



# begin example "glue.fun.tutorial.experiment5"
class Experiment5(glue.Glue.Component2Copper):

    def __init__(self, node, name, phyDataTransmission, phyNotification, **kw):
        super(Experiment5, self).__init__(node, name, phyDataTransmission, phyNotification, **kw)

        buffer = openwns.FUN.Node("unicastBuffer",
                                  openwns.Buffer.Dropping(size = 100,
                                                          lossRatioProbeName = 'glue.unicastBufferLoss',
                                                          sizeProbeName = 'glue.unicastBufferSize',
                                                          parentLogger = self.logger))

        topWindowProbe = openwns.FUN.Node("topWindowProbe",
                                          openwns.Probe.Window("glue.topWindowProbe",
                                                               "glue.top",
                                                               windowSize=.25,
                                                               parentLogger = self.logger))

        topDelayProbe = openwns.FUN.Node("topDelayProbe",
                                         openwns.Probe.Packet("glue.topDelayProbe",
                                                              "glue.top",
                                                              parentLogger = self.logger))

        aloha = openwns.FUN.Node("aloha",
                                 glue.Glue.Aloha(commandName = "aloha",
                                                 maximumWaitingTime = 0.01,
                                                 parentLogger = self.logger))

        crc = openwns.FUN.Node("crc",
                               openwns.CRC.CRC("lowerConvergence",
                                               lossRatioProbeName = 'glue.crcLoss',
                                               parentLogger = self.logger))

        bottomWindowProbe = openwns.FUN.Node("bottomWindowProbe",
                                             openwns.Probe.Window("glue.bottomWindowProbe",
                                                                  "glue.bottom",
                                                                  windowSize=.25,
                                                                  parentLogger = self.logger))

        bottomDelayProbe = openwns.FUN.Node("bottomDelayProbe",
                                            openwns.Probe.Packet("glue.bottomDelayProbe",
                                                                 "glue.bottom",
                                                                 parentLogger = self.logger))


        self.fun.add(buffer)
        self.fun.add(topWindowProbe)
        self.fun.add(topDelayProbe)
        self.fun.add(aloha)
        self.fun.add(crc)
        self.fun.add(bottomWindowProbe)
        self.fun.add(bottomDelayProbe)


        self.fun.connect(self.unicastUpperConvergence, buffer)
        self.fun.connect(buffer, topWindowProbe)
        self.fun.connect(topWindowProbe, topDelayProbe)
        self.fun.connect(topDelayProbe, aloha)
        self.fun.connect(aloha, crc)
        self.fun.connect(crc, bottomWindowProbe)
        self.fun.connect(bottomWindowProbe, bottomDelayProbe)
        self.fun.connect(bottomDelayProbe, self.lowerConvergence)
# end example



# begin example "glue.fun.tutorial.experiment6"
class Experiment6(glue.Glue.Component2Copper):

    def __init__(self, node, name, phyDataTransmission, phyNotification, **kw):
        super(Experiment6, self).__init__(node, name, phyDataTransmission, phyNotification, **kw)

        buffer = openwns.FUN.Node("unicastBuffer",
                                  openwns.Buffer.Dropping(size = 100,
                                                          lossRatioProbeName = 'glue.unicastBufferLoss',
                                                          sizeProbeName = 'glue.unicastBufferSize',
                                                          parentLogger = self.logger))

        topWindowProbe = openwns.FUN.Node("topWindowProbe",
                                          openwns.Probe.Window("glue.topWindowProbe",
                                                               "glue.top",
                                                               windowSize=.25,
                                                               parentLogger = self.logger))

        topDelayProbe = openwns.FUN.Node("topDelayProbe",
                                         openwns.Probe.Packet("glue.topDelayProbe",
                                                              "glue.top",
                                                              parentLogger = self.logger))

        arq = openwns.FUN.Node("arq", openwns.ARQ.StopAndWait(resendTimeout=0.003,
                                                              parentLogger = self.logger))

        arqWindowProbe = openwns.FUN.Node("arqWindowProbe",
                                          openwns.Probe.Window("glue.topWindowProbe",
                                                               "glue.arq",
                                                               windowSize=.25,
                                                               parentLogger = self.logger))

        arqDelayProbe = openwns.FUN.Node("arqDelayProbe",
                                         openwns.Probe.Packet("glue.topDelayProbe",
                                                              "glue.arq",
                                                              parentLogger = self.logger))

        aloha = openwns.FUN.Node("aloha",
                                 glue.Glue.Aloha(commandName = "aloha",
                                                 maximumWaitingTime = 0.01,
                                                 parentLogger = self.logger))

        crc = openwns.FUN.Node("crc",
                               openwns.CRC.CRC("lowerConvergence",
                                               lossRatioProbeName = 'glue.crcLoss',
                                               parentLogger = self.logger))

        bottomWindowProbe = openwns.FUN.Node("bottomWindowProbe",
                                             openwns.Probe.Window("glue.bottomWindowProbe",
                                                                  "glue.bottom",
                                                                  windowSize=.25,
                                                                  parentLogger = self.logger))

        bottomDelayProbe = openwns.FUN.Node("bottomDelayProbe",
                                            openwns.Probe.Packet("glue.bottomDelayProbe",
                                                                 "glue.bottom",
                                                                 parentLogger = self.logger))


        self.fun.add(buffer)
        self.fun.add(topWindowProbe)
        self.fun.add(topDelayProbe)
        self.fun.add(arq)
        self.fun.add(arqWindowProbe)
        self.fun.add(arqDelayProbe)
        self.fun.add(aloha)
        self.fun.add(crc)
        self.fun.add(bottomWindowProbe)
        self.fun.add(bottomDelayProbe)


        self.fun.connect(self.unicastUpperConvergence, buffer)
        self.fun.connect(buffer, topWindowProbe)
        self.fun.connect(topWindowProbe, topDelayProbe)
        self.fun.connect(topDelayProbe, arq)
        self.fun.connect(arq, arqWindowProbe)
        self.fun.connect(arqWindowProbe, arqDelayProbe)
        self.fun.connect(arqDelayProbe, aloha)
        self.fun.connect(aloha, crc)
        self.fun.connect(crc, bottomWindowProbe)
        self.fun.connect(bottomWindowProbe, bottomDelayProbe)
        self.fun.connect(bottomDelayProbe, self.lowerConvergence)
# end example



# begin example "glue.fun.tutorial.experiment7"
class Experiment7(glue.Glue.Component2Copper):

    def __init__(self, node, name, phyDataTransmission, phyNotification, **kw):
        super(Experiment7, self).__init__(node, name, phyDataTransmission, phyNotification, **kw)

        buffer = openwns.FUN.Node("unicastBuffer",
                                  openwns.Buffer.Dropping(size = 100,
                                                          lossRatioProbeName = 'glue.unicastBufferLoss',
                                                          sizeProbeName = 'glue.unicastBufferSize',
                                                          parentLogger = self.logger))

        topWindowProbe = openwns.FUN.Node("topWindowProbe",
                                          openwns.Probe.Window("glue.topWindowProbe",
                                                               "glue.top",
                                                               windowSize=.25,
                                                               parentLogger = self.logger))

        topDelayProbe = openwns.FUN.Node("topDelayProbe",
                                         openwns.Probe.Packet("glue.topDelayProbe",
                                                              "glue.top",
                                                              parentLogger = self.logger))

        arqFU = openwns.ARQ.StopAndWait(resendTimeout=0.003,
                                        parentLogger = self.logger)

        arqFlowSeparatorFU = openwns.FlowSeparator.FlowSeparator(glue.KeyBuilder.KeyBuilder("unicastUpperConvergence"),
                                                                 openwns.FlowSeparator.CreateOnFirstCompound(openwns.FlowSeparator.Config('arq', arqFU)),
                                                                 parentLogger = self.logger)

        arqFlowSeparator = openwns.FUN.Node('flowSeparator', arqFlowSeparatorFU)

        arqWindowProbe = openwns.FUN.Node("arqWindowProbe",
                                          openwns.Probe.Window("glue.topWindowProbe",
                                                               "glue.arq",
                                                               windowSize=.25,
                                                               parentLogger = self.logger))

        arqDelayProbe = openwns.FUN.Node("arqDelayProbe",
                                         openwns.Probe.Packet("glue.topDelayProbe",
                                                              "glue.arq",
                                                              parentLogger = self.logger))

        aloha = openwns.FUN.Node("aloha",
                                 glue.Glue.Aloha(commandName = "aloha",
                                                 maximumWaitingTime = 0.01,
                                                 parentLogger = self.logger))

        crc = openwns.FUN.Node("crc",
                               openwns.CRC.CRC("lowerConvergence",
                                               lossRatioProbeName = 'glue.crcLoss',
                                               parentLogger = self.logger))

        bottomWindowProbe = openwns.FUN.Node("bottomWindowProbe",
                                             openwns.Probe.Window("glue.bottomWindowProbe",
                                                                  "glue.bottom",
                                                                  windowSize=.25,
                                                                  parentLogger = self.logger))

        bottomDelayProbe = openwns.FUN.Node("bottomDelayProbe",
                                            openwns.Probe.Packet("glue.bottomDelayProbe",
                                                                 "glue.bottom",
                                                                 parentLogger = self.logger))


        self.fun.add(buffer)
        self.fun.add(topWindowProbe)
        self.fun.add(topDelayProbe)
        self.fun.add(arqFlowSeparator)
        self.fun.add(arqWindowProbe)
        self.fun.add(arqDelayProbe)
        self.fun.add(aloha)
        self.fun.add(crc)
        self.fun.add(bottomWindowProbe)
        self.fun.add(bottomDelayProbe)


        self.fun.connect(self.unicastUpperConvergence, buffer)
        self.fun.connect(buffer, topWindowProbe)
        self.fun.connect(topWindowProbe, topDelayProbe)
        self.fun.connect(topDelayProbe, arqFlowSeparator)
        self.fun.connect(arqFlowSeparator, arqWindowProbe)
        self.fun.connect(arqWindowProbe, arqDelayProbe)
        self.fun.connect(arqDelayProbe, aloha)
        self.fun.connect(aloha, crc)
        self.fun.connect(crc, bottomWindowProbe)
        self.fun.connect(bottomWindowProbe, bottomDelayProbe)
        self.fun.connect(bottomDelayProbe, self.lowerConvergence)
# end example



# begin example "glue.fun.tutorial.experiment8"
class Experiment8(glue.Glue.Component2Copper):

    def __init__(self, node, name, phyDataTransmission, phyNotification, **kw):
        super(Experiment8, self).__init__(node, name, phyDataTransmission, phyNotification, **kw)

        buffer = openwns.FUN.Node("unicastBuffer",
                                  openwns.Buffer.Dropping(size = 100,
                                                          lossRatioProbeName = 'glue.unicastBufferLoss',
                                                          sizeProbeName = 'glue.unicastBufferSize',
                                                          parentLogger = self.logger))

        topWindowProbe = openwns.FUN.Node("topWindowProbe",
                                          openwns.Probe.Window("glue.topWindowProbe",
                                                               "glue.top",
                                                               windowSize=.25,
                                                               parentLogger = self.logger))

        topDelayProbe = openwns.FUN.Node("topDelayProbe",
                                         openwns.Probe.Packet("glue.topDelayProbe",
                                                              "glue.top",
                                                              parentLogger = self.logger))

        arqFU = openwns.ARQ.StopAndWaitRC(resendTimeout=0.003,
                                          parentLogger = self.logger)

        flowSeparatorFU = openwns.FlowSeparator.FlowSeparator(glue.KeyBuilder.KeyBuilder("unicastUpperConvergence"),
                                                              openwns.FlowSeparator.CreateOnFirstCompound(openwns.FlowSeparator.Config('arq', arqFU)),
                                                              parentLogger = self.logger)

        flowSeparator = openwns.FUN.Node('flowSeparator', flowSeparatorFU)

        arqWindowProbe = openwns.FUN.Node("arqWindowProbe",
                                          openwns.Probe.Window("glue.topWindowProbe",
                                                               "glue.arq",
                                                               windowSize=.25,
                                                               parentLogger = self.logger))

        arqDelayProbe = openwns.FUN.Node("arqDelayProbe",
                                         openwns.Probe.Packet("glue.topDelayProbe",
                                                              "glue.arq",
                                                              parentLogger = self.logger))

        aloha = openwns.FUN.Node("aloha",
                                 glue.Glue.Aloha(commandName = "aloha",
                                                 maximumWaitingTime = 0.01,
                                                 parentLogger = self.logger))

        arqMux = openwns.FUN.Node("arqMux",
                                  openwns.Multiplexer.Dispatcher(opcodeSize = 0,
                                                                 parentLogger=self.logger))

        crc = openwns.FUN.Node("crc",
                               openwns.CRC.CRC("lowerConvergence",
                                               lossRatioProbeName = 'glue.crcLoss',
                                               parentLogger = self.logger))

        bottomWindowProbe = openwns.FUN.Node("bottomWindowProbe",
                                             openwns.Probe.Window("glue.bottomWindowProbe",
                                                                  "glue.bottom",
                                                                  windowSize=.25,
                                                                  parentLogger = self.logger))

        bottomDelayProbe = openwns.FUN.Node("bottomDelayProbe",
                                            openwns.Probe.Packet("glue.bottomDelayProbe",
                                                                 "glue.bottom",
                                                                 parentLogger = self.logger))


        self.fun.add(buffer)
        self.fun.add(topWindowProbe)
        self.fun.add(topDelayProbe)
        self.fun.add(flowSeparator)
        self.fun.add(arqWindowProbe)
        self.fun.add(arqDelayProbe)
        self.fun.add(aloha)
        self.fun.add(arqMux)
        self.fun.add(crc)
        self.fun.add(bottomWindowProbe)
        self.fun.add(bottomDelayProbe)


        self.fun.connect(self.unicastUpperConvergence, buffer)
        self.fun.connect(buffer, topWindowProbe)
        self.fun.connect(topWindowProbe, topDelayProbe)
        self.fun.connect(topDelayProbe, flowSeparator)

        self.fun.connect(flowSeparator, openwns.ARQ.StopAndWaitRC.Data, arqWindowProbe)
        self.fun.connect(arqWindowProbe, arqDelayProbe)
        self.fun.connect(arqDelayProbe, aloha)
        self.fun.connect(aloha, arqMux)

        self.fun.connect(flowSeparator, openwns.ARQ.StopAndWaitRC.Ack, arqMux)

        self.fun.connect(arqMux, crc)
        self.fun.connect(crc, bottomWindowProbe)
        self.fun.connect(bottomWindowProbe, bottomDelayProbe)
        self.fun.connect(bottomDelayProbe, self.lowerConvergence)
# end example



# begin example "glue.fun.tutorial.experiment9"
class Experiment9(glue.Glue.Component2Copper):

    def __init__(self, node, name, phyDataTransmission, phyNotification, **kw):
        super(Experiment9, self).__init__(node, name, phyDataTransmission, phyNotification, **kw)

        buffer = openwns.FUN.Node("unicastBuffer",
                                  openwns.Buffer.Dropping(size = 100,
                                                          lossRatioProbeName = 'glue.unicastBufferLoss',
                                                          sizeProbeName = 'glue.unicastBufferSize',
                                                          parentLogger = self.logger))

        topWindowProbe = openwns.FUN.Node("topWindowProbe",
                                          openwns.Probe.Window("glue.topWindowProbe",
                                                               "glue.top",
                                                               windowSize=.25,
                                                               parentLogger = self.logger))

        topDelayProbe = openwns.FUN.Node("topDelayProbe",
                                         openwns.Probe.Packet("glue.topDelayProbe",
                                                              "glue.top",
                                                              parentLogger = self.logger))

        subFUN = openwns.FUN.FUN()

        sar = openwns.FUN.Node("sar", openwns.SAR.Fixed(segmentSize = 256,
                                                        parentLogger = self.logger))

        arq = openwns.FUN.Node("arq", openwns.ARQ.StopAndWaitRC(resendTimeout=0.003,
                                                                parentLogger = self.logger))

        subFUN.add(sar)
        subFUN.add(arq)

        subFUN.connect(sar, arq)

        groupFU = openwns.Group.Group(subFUN, "sar")
        groupFU.bottomPorts.append(openwns.Group.PortConnector("arq",
                                                               openwns.ARQ.StopAndWaitRC.Data,
                                                               openwns.ARQ.StopAndWaitRC.Data))
        groupFU.bottomPorts.append(openwns.Group.PortConnector("arq",
                                                               openwns.ARQ.StopAndWaitRC.Ack,
                                                               openwns.ARQ.StopAndWaitRC.Ack))

        flowSeparatorFU = openwns.FlowSeparator.FlowSeparator(glue.KeyBuilder.KeyBuilder("unicastUpperConvergence"),
                                                              openwns.FlowSeparator.CreateOnFirstCompound(openwns.FlowSeparator.Config('group', groupFU)),
                                                              parentLogger = self.logger)

        flowSeparator = openwns.FUN.Node('flowSeparator', flowSeparatorFU)

        arqWindowProbe = openwns.FUN.Node("arqWindowProbe",
                                          openwns.Probe.Window("glue.arqWindowProbe",
                                                               "glue.arq",
                                                               windowSize=.25,
                                                               parentLogger = self.logger))

        arqDelayProbe = openwns.FUN.Node("arqDelayProbe",
                                         openwns.Probe.Packet("glue.arqDelayProbe",
                                                              "glue.arq",
                                                              parentLogger = self.logger))

        aloha = openwns.FUN.Node("aloha",
                                 glue.Glue.Aloha(commandName = "aloha",
                                                 maximumWaitingTime = 0.01,
                                                 parentLogger = self.logger))

        arqMux = openwns.FUN.Node("arqMux",
                                  openwns.Multiplexer.Dispatcher(opcodeSize = 0,
                                                                 parentLogger=self.logger))

        crc = openwns.FUN.Node("crc",
                               openwns.CRC.CRC("lowerConvergence",
                                               lossRatioProbeName = 'glue.crcLoss',
                                               parentLogger = self.logger))

        bottomWindowProbe = openwns.FUN.Node("bottomWindowProbe",
                                             openwns.Probe.Window("glue.bottomWindowProbe",
                                                                  "glue.bottom",
                                                                  windowSize=.25,
                                                                  parentLogger = self.logger))

        bottomDelayProbe = openwns.FUN.Node("bottomDelayProbe",
                                            openwns.Probe.Packet("glue.bottomDelayProbe",
                                                                 "glue.bottom",
                                                                 parentLogger = self.logger))


        self.fun.add(buffer)
        self.fun.add(topWindowProbe)
        self.fun.add(topDelayProbe)
        self.fun.add(flowSeparator)
        self.fun.add(arqWindowProbe)
        self.fun.add(arqDelayProbe)
        self.fun.add(aloha)
        self.fun.add(arqMux)
        self.fun.add(crc)
        self.fun.add(bottomWindowProbe)
        self.fun.add(bottomDelayProbe)


        self.fun.connect(self.unicastUpperConvergence, buffer)
        self.fun.connect(buffer, topWindowProbe)
        self.fun.connect(topWindowProbe, topDelayProbe)
        self.fun.connect(topDelayProbe, flowSeparator)

        self.fun.connect(flowSeparator, openwns.ARQ.StopAndWaitRC.Data, arqWindowProbe)
        self.fun.connect(arqWindowProbe, arqDelayProbe)
        self.fun.connect(arqDelayProbe, aloha)
        self.fun.connect(aloha, arqMux)

        self.fun.connect(flowSeparator, openwns.ARQ.StopAndWaitRC.Ack, arqMux)

        self.fun.connect(arqMux, crc)
        self.fun.connect(crc, bottomWindowProbe)
        self.fun.connect(bottomWindowProbe, bottomDelayProbe)
        self.fun.connect(bottomDelayProbe, self.lowerConvergence)
# end example
