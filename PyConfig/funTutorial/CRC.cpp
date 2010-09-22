/*******************************************************************************
 * This file is part of openWNS (open Wireless Network Simulator)
 * _____________________________________________________________________________
 *
 * Copyright (C) 2004-2007
 * Chair of Communication Networks (ComNets)
 * Kopernikusstr. 5, D-52074 Aachen, Germany
 * phone: ++49-241-80-27910,
 * fax: ++49-241-80-22242
 * email: info@openwns.org
 * www: http://www.openwns.org
 * _____________________________________________________________________________
 *
 * openWNS is free software; you can redistribute it and/or modify it under the
 * terms of the GNU Lesser General Public License version 2 as published by the
 * Free Software Foundation;
 *
 * openWNS is distributed in the hope that it will be useful, but WITHOUT ANY
 * WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
 * A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
 * details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 ******************************************************************************/

#include <GLUE/CRC.hpp>

using namespace glue;

STATIC_FACTORY_REGISTER_WITH_CREATOR(CRC, FunctionalUnit, "glue.CRC", FUNConfigCreator);

CRC::CRC(fun::FUN* fuNet, const wns::pyconfig::View& config):
    wns::ldk::CommandTypeSpecifier<>(fuNet),
    wns::ldk::HasReceptor<>(),
    wns::ldk::HasConnector<>(),
    wns::ldk::HasDeliverer<>(),
    wns::ldk::Cloneable<CRC>()
{
}

void
CRC::doSendData(const wns::ldk::CompoundPtr& compound)
{
    getConnector()->getAcceptor(compound->copy())->sendData(compound);
}

bool
CRC::doIsAccepting(const wns::ldk::CompoundPtr& compound) const
{
    return getConnector()->hasAcceptor(compound);
}

void
CRC::doWakeup()
{
    getReceptor()->wakeup();
}

void
CRC::doOnData(const wns::ldk::CompoundPtr& compound)
{
    // Place your code here
}
