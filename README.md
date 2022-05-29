# VE.bus SMA Sunny Home Manager service

This project was inspired by the idea to use an existing SMA Sunny Home Manager 2.0 (SHM) as energy meter for a Victron Energy GX device, e.g. Venus OS running on a Raspberry Pi.

Sean Mitchell realized a very similar project in Go https://github.com/mitchese/shm-et340, but I wanted to have this code in Python.

This Python-Code is based on https://github.com/victronenergy/velib_python/blob/master/dbusdummyservice.py and translates the SHM data received via speedwire to the VE.bus. More information on D-Bus API definition here: https://github.com/victronenergy/venus/wiki/dbus-api

SMA PV converters are supported by Venus OS and automtically visible in the Venus OS main screen, e.g. like this:
![grafik](https://user-images.githubusercontent.com/99689771/170887647-da0df145-88f0-4e5a-af75-35568bd16417.png)

To install an AC connected electric energy storage (ESS) with VE components, an Energy Meter is required. Unfurtunately the SMA Energy Meter called SunnyHomeManager 2.0 (SHM) is not supported by Venus OS. This Python code allows to use the data from an existing SMA SHM within Venus OS.

Via speedwire communication all data are read from the SHM and transfered to the D-Bus. This Python-Code runs on the Raspberry Pi where Venus OS is installed and running. You need to establish root access to Venus OS first, see https://www.victronenergy.com/live/ccgx:root_access.

As soon as this Python code is running, the SMA SHM is listed in the Venus OS Device List, e.g. like this:
![grafik](https://user-images.githubusercontent.com/99689771/170887921-95d5f11c-5d39-4c7b-bace-c404df5d5f12.png)

The measured electric power on the individual three phases are visible on the Venus OS main screen!

On Venus OS console the output of ths Python code may look like this (OBIS id in brackets):

Phase      ------- L1 ------ ------- L2 ------ ------- L3 ------<br>
Power         89.8 (21.4.0)     94.6 (41.4.0)    346.7 (61.4.0) W<br>
Current      12.84 (31.4.0)     7.22 (51.4.0)    16.10 (71.4.0) A<br>
Voltage    231.529 (32.4.0)  232.207 (52.4.0)  232.865 (72.4.0) V<br>
Energy +    XX12.5 (21.8.0)   XX38.1 (41.8.0)   XX27.9 (61.8.0) kWh<br>
Energy -    XX02.2 (22.8.0)   XX22.4 (42.8.0)   XX08.4 (62.8.0) kWh<br>
INFO:root:House Consumption: 531.1
