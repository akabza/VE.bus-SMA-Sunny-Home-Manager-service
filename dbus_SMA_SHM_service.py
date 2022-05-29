#!/usr/bin/env python3

"""

Created by Alexander Kabza, based on https://github.com/victronenergy/velib_python/blob/master/dbusdummyservice.py

Virtual Device to read SMA Sunny Home Manager 2.0 and use this as Energy Meter for Victron Energy Venus OS

2022-02-28  first version, created based on https://github.com/victronenergy/velib_python/blob/master/dbusdummyservice.py
2022-03-01  minor modifications
2022-04-18  changed "servicename='com.victronenergy.grid'," to "servicename='com.victronenergy.grid.cgwacs_ttyUSB0_di30_mb1',"
2022-05-29  removed number format for '/Ac/Lx/Power' to finally get this code running!

"""
from gi.repository import GLib
import sys
import os
import logging
import socket
import struct

# our own packages
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '../ext/velib_python'))
from vedbus import VeDbusService

# ip for SMA Sunny Home Manager 2.0
MULTICAST_IP = "239.12.255.254"
MULTICAST_PORT = 9522

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("", MULTICAST_PORT))

mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_IP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# global variables from SMA Sunny Home Manager 2.0
SerialNo = ""
VoltageL1 = 0.0
VoltageL2 = 0.0
VoltageL3 = 0.0
CurrentL1 = 0.0
CurrentL2 = 0.0
CurrentL3 = 0.0
PowerL1 = 0.0
PowerL2 = 0.0
PowerL3 = 0.0
EnergyForwardL1 = 0.0
EnergyReverseL1 = 0.0
EnergyForwardL2 = 0.0
EnergyReverseL2 = 0.0
EnergyForwardL3 = 0.0
EnergyReverseL3 = 0.0
PowerTotal = 0.0
EnergyForward = 0.0
EnergyReverse = 0.0


def getvalue(hexStr, search, length):
    pos = hexStr.find(search)
    if (pos != -1):
        pos = pos + len(search)
        value = hexStr[pos:pos + length]
        try:
            floatvalue = float(int(value, 16))
        except:
            floatvalue = 0.0
        return floatvalue
    else:
        floatvalue = 0.0
        return floatvalue
# --- def getvalue


def decode_speedwire(data):

    global SerialNo
    global VoltageL1
    global VoltageL2
    global VoltageL3
    global CurrentL1
    global CurrentL2
    global CurrentL3
    global PowerL1
    global PowerL2
    global PowerL3
    global EnergyForwardL1
    global EnergyReverseL1
    global EnergyForwardL2
    global EnergyReverseL2
    global EnergyForwardL3
    global EnergyReverseL3
    global PowerTotal
    global EnergyForward
    global EnergyReverse

    SMA = data[0:3]  # This is just the identifier of the packet, should start with "SMA\0"
    sysUid = data[4:7]
    serialNumber = data[20:24]
    #print("SMA: " + str(SMA) + " sysUid: " + str(sysUid) + " Serial: " + str(serialNumber.hex()))

    hexStr = ""
    for onebyte in data: hexStr += f"{onebyte:02x}"
    #print(hexStr)

    SerialNo = str(int(hexStr[40:48], 16))

    P_pos = getvalue(hexStr, "010400", 8) / 10
    P_neg = getvalue(hexStr, "020400", 8) / 10
    PowerTotal = P_pos - P_neg
    E_pos = getvalue(hexStr, "010800", 16) / 3600000
    EnergyForward = E_pos
    E_neg = getvalue(hexStr, "020800", 16) / 3600000
    EnergyReverse = E_neg
    Pb_pos = getvalue(hexStr, "030400", 8) / 10
    Pb_neg = getvalue(hexStr, "040400", 8) / 10
    Eb_pos = getvalue(hexStr, "030800", 16) / 3600000
    Eb_neg = getvalue(hexStr, "040800", 16) / 3600000
    Ps_pos = getvalue(hexStr, "090400", 8) / 10
    Ps_neg = getvalue(hexStr, "0a0400", 8) / 10
    Es_pos = getvalue(hexStr, "090800", 16) / 3600000
    Es_neg = getvalue(hexStr, "0a0800", 16) / 3600000
    phi = getvalue(hexStr, "0d0400", 8) / 10

    P1_pos = getvalue(hexStr, "150400", 8) / 10
    P1_neg = getvalue(hexStr, "160400", 8) / 10
    PowerL1 = P1_pos - P1_neg
    P2_pos = getvalue(hexStr, "290400", 8) / 10
    P2_neg = getvalue(hexStr, "2a0400", 8) / 10
    PowerL2 = P2_pos - P2_neg
    P3_pos = getvalue(hexStr, "3d0400", 8) / 10
    P3_neg = getvalue(hexStr, "3e0400", 8) / 10
    PowerL3 = P3_pos - P3_neg
    EnergyForwardL1 = getvalue(hexStr, "150800", 16) / 3600000
    EnergyReverseL1 = getvalue(hexStr, "160800", 16) / 3600000
    EnergyForwardL2 = getvalue(hexStr, "290800", 16) / 3600000
    EnergyReverseL2 = getvalue(hexStr, "2a0800", 16) / 3600000
    EnergyForwardL3 = getvalue(hexStr, "3d0800", 16) / 3600000
    EnergyReverseL3 = getvalue(hexStr, "3e0800", 16) / 3600000
    CurrentL1 = getvalue(hexStr, "1f0400", 8) / 1000
    CurrentL2 = getvalue(hexStr, "330400", 8) / 1000
    CurrentL3 = getvalue(hexStr, "470400", 8) / 1000
    VoltageL1 = getvalue(hexStr, "200400", 8) / 1000
    VoltageL2 = getvalue(hexStr, "340400", 8) / 1000
    VoltageL3 = getvalue(hexStr, "480400", 8) / 1000
    try:
        CurrentL1 = PowerL1 / VoltageL1
        CurrentL2 = PowerL2 / VoltageL2
        CurrentL3 = PowerL3 / VoltageL3
    except:    
        CurrentL1 = 0.0
        CurrentL2 = 0.0
        CurrentL3 = 0.0
    phi1 = getvalue(hexStr, "210400", 8) / 10
    phi2 = getvalue(hexStr, "350400", 8) / 10
    phi3 = getvalue(hexStr, "490400", 8) / 10    


class DbusDummyService(object):
    #def __init__(self, servicename, deviceinstance, paths, productname='SMA Sunny Home Manager 2.0', connection='/dev/ttyUSB0'):
    def __init__(self, servicename, deviceinstance, paths, productname='SMA Sunny Home Manager 2.0', connection='/dev/ttyUSB0'):
        self._dbusservice = VeDbusService(servicename)
        self._paths = paths

        logging.debug("%s /DeviceInstance = %d" % (servicename, deviceinstance))

        # Create the management objects, as specified in the ccgx dbus-api document
        self._dbusservice.add_path('/Mgmt/ProcessName', __file__)
        self._dbusservice.add_path('/Mgmt/ProcessVersion', '0.1')
        self._dbusservice.add_path('/Mgmt/Connection', connection)

        # Create the mandatory objects
        self._dbusservice.add_path('/DeviceInstance', deviceinstance)
        self._dbusservice.add_path('/ProductId', 45069) # value used in ac_sensor_bridge.cpp of dbus-cgwacs
        self._dbusservice.add_path('/ProductName', productname)
        self._dbusservice.add_path('/FirmwareVersion', 0.1)
        self._dbusservice.add_path('/HardwareVersion', 0)
        self._dbusservice.add_path('/Connected', 1)
        

        for path, settings in self._paths.items():
            self._dbusservice.add_path(
                path, settings['initial'], writeable=True, onchangecallback=self._handlechangedvalue)

        GLib.timeout_add(1000, self._update)


    def _update(self):

        decode_speedwire(sock.recv(10240))

        #print("\nPhase      ------- L1 ------ ------- L2 ------ ------- L3 ------")
        #print("Power      {0:7.1f} (21.4.0)  {1:7.1f} (41.4.0)  {2:7.1f} (61.4.0) W".format(PowerL1, PowerL2, PowerL3))
        #print("Current    {0:7.2f} (31.4.0)  {1:7.2f} (51.4.0)  {2:7.2f} (71.4.0) A".format(CurrentL1, CurrentL2, CurrentL3))
        #print("Voltage    {0:7.3f} (32.4.0)  {1:7.3f} (52.4.0)  {2:7.3f} (72.4.0) V".format(VoltageL1, VoltageL2, VoltageL3))
        #print("Energy +   {0:7.1f} (21.8.0)  {1:7.1f} (41.8.0)  {2:7.1f} (61.8.0) kWh".format(EnergyForwardL1, EnergyForwardL2, EnergyForwardL3))
        #print("Energy -   {0:7.1f} (22.8.0)  {1:7.1f} (42.8.0)  {2:7.1f} (62.8.0) kWh".format(EnergyReverseL1, EnergyReverseL2, EnergyReverseL3))
        
        if (PowerL1 * PowerL2 * PowerL3 != 0):
            self._dbusservice['/Ac/L1/Voltage'] = '{0:0.2f}V'.format(VoltageL1)
            self._dbusservice['/Ac/L2/Voltage'] = '{0:0.2f}V'.format(VoltageL2)
            self._dbusservice['/Ac/L3/Voltage'] = '{0:0.2f}V'.format(VoltageL3)
            self._dbusservice['/Ac/L1/Current'] = '{0:0.2f}A'.format(CurrentL1)
            self._dbusservice['/Ac/L2/Current'] = '{0:0.2f}A'.format(CurrentL2)
            self._dbusservice['/Ac/L3/Current'] = '{0:0.2f}A'.format(CurrentL3)
            self._dbusservice['/Ac/L1/Power'] = PowerL1    # no format here!!!
            self._dbusservice['/Ac/L2/Power'] = PowerL2    # no format here!!!
            self._dbusservice['/Ac/L3/Power'] = PowerL3    # no format here!!!
            self._dbusservice['/Ac/L1/Energy/Forward'] = '{0:0.2f}kWh'.format(EnergyForwardL1)
            self._dbusservice['/Ac/L2/Energy/Forward'] = '{0:0.2f}kWh'.format(EnergyForwardL2)
            self._dbusservice['/Ac/L3/Energy/Forward'] = '{0:0.2f}kWh'.format(EnergyForwardL3)
            self._dbusservice['/Ac/L1/Energy/Reverse'] = '{0:0.2f}kWh'.format(EnergyReverseL1)
            self._dbusservice['/Ac/L2/Energy/Reverse'] = '{0:0.2f}kWh'.format(EnergyReverseL2)
            self._dbusservice['/Ac/L3/Energy/Reverse'] = '{0:0.2f}kWh'.format(EnergyReverseL3)
            self._dbusservice['/Ac/Energy/Forward'] = '{0:0.2f}kWh'.format(EnergyForward)
            self._dbusservice['/Ac/Energy/Reverse'] = '{0:0.2f}kWh'.format(EnergyReverse)
            self._dbusservice['/Ac/Power'] = '{0:0.2f}W'.format(PowerTotal)  # positive: consumption, negative: feed into grid
            self._dbusservice['/Ac/Current'] = '{0:0.2f}A'.format(CurrentL1 + CurrentL2 + CurrentL3)
        logging.info("House Consumption: %sW" % (PowerTotal))
        return True

    def _handlechangedvalue(self, path, value):
        logging.debug("someone else updated %s to %s" % (path, value))
        return True # accept the change


# === All code below is to simply run it from the commandline for debugging purposes ===

# It will created a dbus service called com.victronenergy.pvinverter.output.
# To try this on commandline, start this program in one terminal, and try these commands
# from another terminal:
# dbus com.victronenergy.pvinverter.output
# dbus com.victronenergy.pvinverter.output /Ac/Energy/Forward GetValue
# dbus com.victronenergy.pvinverter.output /Ac/Energy/Forward SetValue %20
#
# Above examples use this dbus client: http://code.google.com/p/dbus-tools/wiki/DBusCli
# See their manual to explain the % in %20

def main():
    logging.basicConfig(level=logging.DEBUG)

    from dbus.mainloop.glib import DBusGMainLoop
    # Have a mainloop, so we can send/receive asynchronous calls to and from dbus
    DBusGMainLoop(set_as_default=True)

    pvac_output = DbusDummyService(
        servicename='com.victronenergy.grid.SMAHomeManager',   # add what you want here, but not just 'com.victronenergy.grid', also 'com.victronenergy.grid.X' works
        deviceinstance=0,
        paths={
          '/Ac/Power': {'initial': 0},
          '/Ac/Current': {'initial': 0},
          '/Ac/L1/Voltage': {'initial': 0},
          '/Ac/L2/Voltage': {'initial': 0},
          '/Ac/L3/Voltage': {'initial': 0},
          '/Ac/L1/Current': {'initial': 0},
          '/Ac/L2/Current': {'initial': 0},
          '/Ac/L3/Current': {'initial': 0},
          '/Ac/L1/Power': {'initial': 0},
          '/Ac/L2/Power': {'initial': 0},
          '/Ac/L3/Power': {'initial': 0},
          '/Ac/L1/Energy/Forward': {'initial': 0},
          '/Ac/L2/Energy/Forward': {'initial': 0},
          '/Ac/L3/Energy/Forward': {'initial': 0},
          '/Ac/L1/Energy/Reverse': {'initial': 0},
          '/Ac/L2/Energy/Reverse': {'initial': 0},
          '/Ac/L3/Energy/Reverse': {'initial': 0},
          '/Ac/Energy/Forward': {'initial': 0}, # energy bought from the grid
          '/Ac/Energy/Reverse': {'initial': 0}, # energy sold to the grid
        })

    logging.info('Connected to dbus, and switching over to GLib.MainLoop() (= event based)')
    mainloop = GLib.MainLoop()
    mainloop.run()


if __name__ == "__main__":
    main()