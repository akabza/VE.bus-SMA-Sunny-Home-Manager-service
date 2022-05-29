# VE.bus SMA Sunny Home Manager service

This project was inspired by the idea to use an existing SMA Sunny Home Manager 2.0 (SHM) as energy meter for a Victron Energy GX device, e.g. Venus OS running on a Raspberry Pi.

Sean Mitchell realized a very similar project in Go https://github.com/mitchese/shm-et340, but I wanted to have this code in Python.

This Python-Code is based on https://github.com/victronenergy/velib_python/blob/master/dbusdummyservice.py and translates the SHM data received via speedwire to the VE.bus. More information on D-Bus API definition here: https://github.com/victronenergy/venus/wiki/dbus-api

Via speedwire communication all data are read from the SHM and translated to the D-Bus. This Python-Code runs on the Raspberry Pi where Venus OS is installed and running. Inside the Venus OS menu the SHM device is visible, e.g. like this:

![grafik](https://user-images.githubusercontent.com/99689771/156237997-9427df11-6b66-4b99-82a3-6f5dbfb0c146.png)

On VenusOS it looks like this (OBIS id in brackets):

Phase      ------- L1 ------ ------- L2 ------ ------- L3 ------<br>
Power         89.8 (21.4.0)     94.6 (41.4.0)    346.7 (61.4.0) W<br>
Current      12.84 (31.4.0)     7.22 (51.4.0)    16.10 (71.4.0) A<br>
Voltage    231.529 (32.4.0)  232.207 (52.4.0)  232.865 (72.4.0) V<br>
Energy +    XX12.5 (21.8.0)   XX38.1 (41.8.0)   XX27.9 (61.8.0) kWh<br>
Energy -    XX02.2 (22.8.0)   XX22.4 (42.8.0)   XX08.4 (62.8.0) kWh<br>
INFO:root:House Consumption: 531.1

OPEN ISSUE: I don´t know how to get this data from DeviceInstance 30 (which is used here!) "translated" to DeviceInstance 100. Therefore grid data are NOT vsible in the Venus OS main screen, and also not available for ESS!!! I need support here!
