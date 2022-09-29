# Temp-Monitor---Piico
This project is to build a fully remotely managed temperature monitoring station that hosts its own webpage for configuration and has an API to provide average temperatures over the last 5 minutes.

# Components:

 - 1x ESP 8266 Wemos D1 Mini 
	 - https://www.ebay.com.au/itm/324375676231
 - 1x 30mm Raspberry Pi Cooling Fan 
	 - https://core-electronics.com.au/cooling-fan-for-raspberry-pi.html
 - 1x N-Chanel Mosfet driver 
	 - https://core-electronics.com.au/freetronics-n-mosfet-driver-output-module.html
 - 1x PiicoDev Precision Temperature Sensor TMP117 
	 - https://core-electronics.com.au/piicodev-precision-temperature-sensor-tmp117.html
 - 1x PiicoDev Cable 200mm 
	 - https://core-electronics.com.au/piicodev-cable-200mm.html
 - 1x Heymix USB Charger 
	 - https://www.amazon.com.au/HEYMIX-Charger-Dual-Port-2-Pack-Certificated/dp/B09MFCZWYQ
 - 1x 10cm USB Micro lead
	 - https://www.ebay.com.au/itm/283170488593

# Tools:

 - List item
 - Soldering Iron
 - 3D Printer
 - Snips
 - Needle Nose Pliers
 - Precision Screwdriver Set
 
# Process:
1. 3D Print the enclosure, I used my Creality Ender 3 S1 Pro with a 0.4mm nozzel using eSun PLA+ White filament. There are 3 components in the STL file; a main body, a friction fit back cover and a holder for the piicoDev TMP 117.
2. While the enclosure is printing setup the ESP8266 with micropython and setup WebREPL. 
	(https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html#intro)
3. You should setup a static IP for the ESP8266 in your home wifi router so that it remains constant over time. 
4. Once the ESP8266 is configured and connected to your network log into it using WebREPL and upload the files from this Project (except the stl file for the enclosure and this readme file). **Make sure to update _WiFiManager.py with your SSID and Password before you upload, otherwise the ESP8266 won't reconnect to your network once it reboots!**
6. Snip the PiicoDev Cable in half, since we only need a connector on one end and bare wires on the other. Also snip the fan wire in half as it's quite long and we also need bare wires.
7. Solder all of the components together:<br/>
	**PiicoDev Cable:**<br/>
		Blue -> D2<br/>
		Yellow -> D1<br/>
		Red -> 3.3v<br/>
		Black -> Ground<br/>
		<br/>
	**Fan:**<br/>
		Red -> 3.3v<br/>
		Black -> Drain on N Channel Mosfet<br/>
		<br/>
	**Mosfet:**<br/>
		Drain -> Black fan lead<br/>
		Gate -> D6<br/>
		Source -> Ground<br/>
8. Mount the PiicoDev TMP117 in the printed holder.
9. Insert the screws for the fan through the holes from the front (so the head sits in the cavity flush with the front).
10. Mount the fan on the screws making sure the label is facing the back and tighten the nuts.
11. Next insert the usb charger, to give a really tight friction fit add a very small amount of bluetac on each side and press in, once fully inserted, scrap off the bluetac that has squeezed out.
12. Plug the usb lead into the usb charger and the ESP8266, then insert the ESP8266 into the slot just below the USB housing, the chip should face down and fit into the bridge like holder, the wifi antenna flat black bit with the gold squiggle should slot into the gap at the base of the holder. Also stick the mosfet to the upper side of the case (above the vent holes, I use a tiny amount of bluetac for this as well as the PiicoDev holder).
13. Finally stick the PiicoDev holder to the enclosure at the bottom towards the back and in-line the the airflow from the fan.
14. Push the back cover on, it should be a relatively tight friction fit between the case and the 4 nubbins on the lid. 
15. Plug the completed unit into a power socket in the location you want to monitor. The ESP8266 should boot up and begin hosting the web server on it's IP address.

# API / Endpoints:
There are 5 current endpoints on the hosted webserver (in addition to root /).

 1. /Update<br/>
	 This end point is used to update the location of the temperature monitor and takes a single parameter of 'location'<br/>
	 For example:<br/>
	 [ESP8266IP]/Update?location=Lounge<br/>
	 would update the location to 'Lounge'<br/>
 2. /ToggleFan<br/>
	 This end point is used to toggle fan on and off
3. /GetData<br/>
	This end point will return a JSON object in the format:<br/>
	{<br/>
		"location": [Location as a String], <br/>
		"time": [Current **UTC** time as a string in the format: yyyy-mm-dd HH:MM:SS], <br/>
		"averageTemp": [Average temp over the last 5 minutes as a float], <br/>
		"fan": ["On" or "Off" depending on current fan status]<br/>
	}<br/>
4. /Reboot<br/>
	This end point will trigger the ESP8266 to reboot after 1 second, I generally call this every week or so to avoid any potential memory leak issues etc.<br/>
5.  /RamStatus<br/>
	This is only really used for debugging, since the ESP8266 is very memory constrained I have this function in all my ESP8266 projects. Once called it will trigger a call to mem_info(1) which will print out the current memory (ram) stack data to the WebREPL connection. To use this, first open a WebREPL connection to the ESP8266 and then in another tab call the /RamStatus URL. The memory utilisation will then be printed to your WebREPL console. For this project since a single temp monitor is not very ram intensive this shouldn't be required. But can be very helpful with larger projects.
