# Victron Energy D-Bus for SMA Sunny Home Manager

This project was inspired by the idea to use an existing SMA Sunny Home Manager 2.0 (SHM) as energy meter for a Victron Energy GX device, e.g. Venus OS running on a Raspberry Pi.

This Python-Code is based on https://github.com/victronenergy/velib_python/blob/master/dbusdummyservice.py

Via speedwire communication all data are read from the SHM and translated to the D-Bus. This Python-Code runs on the Raspberry Pi where Venus OS is installed. Inside the Venus OS menu the SHM device is visible.

![grafik](https://user-images.githubusercontent.com/99689771/156237997-9427df11-6b66-4b99-82a3-6f5dbfb0c146.png)
