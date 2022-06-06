# Victron Energy VE.bus SMA Sunny Home Manager service

## Overview

This project was inspired by the idea to use an existing SMA Sunny Home Manager 2.0 (SHM) as energy meter for a Victron Energy GX device, e.g. Venus OS running on a Raspberry Pi.

Sean Mitchell realized a very similar project in Go https://github.com/mitchese/shm-et340, but I wanted to have this code in Python.

This Python-Code is based on https://github.com/victronenergy/velib_python/blob/master/dbusdummyservice.py and translates the SHM data received via speedwire to the VE.bus. More information on D-Bus API definition here: https://github.com/victronenergy/venus/wiki/dbus-api

To install an AC connected electric energy storage (ESS) with VE components, an Energy Meter is required. Unfurtunately the SMA Energy Meter called SunnyHomeManager 2.0 (SHM) is not supported by Venus OS. This Python code allows to use the data from an existing SMA SHM within Venus OS.

## Installation of dummy environment

Also without any Victron Energy component at all you can test this Python code. The only required haerdware is an suitable Raspberry Pi and the SMA Sunny Home Manager 2.0. Do the installation as following:

First, install VenusOS on a suitable Raspberry Pi according to this documentation: https://github.com/victronenergy/venus/wiki/raspberrypi-install-venus-image
Enter the IP of your Respberry Pi running Venus OS, then you see this screen first:
![grafik](https://user-images.githubusercontent.com/99689771/172068270-8edd7571-ba87-4058-ad5e-717005e8a3e4.png)

Second, you need to establish root access to Venus OS first, see https://www.victronenergy.com/live/ccgx:root_access. If this was successful, you can directly work with the terminal, which may look like this:
![grafik](https://user-images.githubusercontent.com/99689771/172068413-b32dc07e-ddc8-41b7-a9d0-e18b993ee456.png)

Third, you may want to scan for an existing PV inverter (or any other existing harware). Go to Settings -> PV inverter -> Scan. If this was successful, your PV inverter is visible on the Venus OS device list and the Venus OS main screen may look like this:
![grafik](https://user-images.githubusercontent.com/99689771/172179033-5d211217-5d94-479f-961e-b042b2eee04b.png)

Forth, you need to copy this Python code to your Raspberry Pi running Venus OS. Also copy vedbus.py and ve_utils.py from this link: https://github.com/victronenergy/velib_python into your (roots) home directory /root/home. 

Fifth, start and test this Python code. If everything works, electric power from the SMA SHM electric grid meter is shown in the Venus OS main screen, red window AC Input. Also the AC Loads are calculated and displayed in the green window, e.g. like this:
![grafik](https://user-images.githubusercontent.com/99689771/172180161-d3f181e0-1fad-4c67-b23d-f95d5472e883.png)

## How it works

Via speedwire communication all data are read from the SHM and transfered to the D-Bus. This Python-Code runs on the Raspberry Pi where Venus OS is installed and running. 

As soon as this Python code is running, the SMA SHM is listed in the Venus OS Device List, e.g. like this:
![grafik](https://user-images.githubusercontent.com/99689771/172181418-8fe93226-d594-482e-9734-b62cdc7a41ae.png)

By selecting the SMA SHM device, e.g. this parameters are visible: 
![grafik](https://user-images.githubusercontent.com/99689771/172180408-aee7bfd6-809f-4100-bc0d-a558abf16c44.png)

The measured electric power on the individual three phases are visible on the Venus OS main screen!

On Venus OS console the output of the Python code may look like this (OBIS id in brackets):

Phase      ------- L1 ------ ------- L2 ------ ------- L3 ------<br>
Power         89.8 (21.4.0)     94.6 (41.4.0)    346.7 (61.4.0) W<br>
Current      12.84 (31.4.0)     7.22 (51.4.0)    16.10 (71.4.0) A<br>
Voltage    231.529 (32.4.0)  232.207 (52.4.0)  232.865 (72.4.0) V<br>
Energy +    XX12.5 (21.8.0)   XX38.1 (41.8.0)   XX27.9 (61.8.0) kWh<br>
Energy -    XX02.2 (22.8.0)   XX22.4 (42.8.0)   XX08.4 (62.8.0) kWh<br>
INFO:root:House Consumption: 531.1
